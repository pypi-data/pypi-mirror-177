import json
import logging
import re
from typing import AsyncIterator, List

import httpx

from .exceptions import (
    StreamNotCreatedException,
    StreamNotDeletedException,
    StreamSubscriptionException,
)
from .sseclient import WicaSSEClient
from .utils import WicaChannel, WicaMessage, WicaStreamProperties


class WicaStream(object):
    """An asynchronous version of the WicaStream object.

    An object of this class represents a single stream from an wica-http server.

    Usage:

    ```python
    >>> stream = wica_api.AsyncWicaStream(channels="EXAMPLE:CHANNEL:123")
    >>> async for message in stream.subscribe():
    >>>     print(message)
    ```

    Parameters:
        channels (List[str]|List[WicaChannel]): The channel or channels the stream should include. Optional parameters can be given per channel with the `WicaChannel` object.
                                                If only one channel is needed just encapsulate it.
        base_url (str): The endpoint the request should be sent to. Usually it has the form `SERVER:PORT/ca/streams`.
        stream_properties (WicaStreamProperties): The properties the stream should have. See `WicaStreamProperties` class for more info.

    """

    def __init__(
        self,
        channels: List[str] | List[WicaChannel],
        stream_properties: WicaStreamProperties | None = None,
        base_url: str = "127.0.0.1/ca/streams",
    ) -> None:
        self.id: int = None
        self.base_url = base_url
        self.channels = [
            WicaChannel(name=channel) if isinstance(channel, str) else channel
            for channel in channels
        ]
        self.stream_properties = stream_properties
        self._logger = logging.getLogger(self.__class__.__module__)
        self._logger.debug(
            f"Initialized AsyncWicaStream for channels {channels} with base_url {base_url}"
        )

    async def create(self):
        """Create a stream from the wica-http server.

        This method can be used to pre-create streams before subscribing. It sends a POST request to the server and gets an ID.
        This ID is than written to the id field of the object and returned.

        Usage:

        ```python
        >>> for _ in range(10):
        >>>     wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])
        >>>     streams.append(wica_stream)
        >>>     await wica_stream.create()
        >>>
        >>> print("Doing someting else before starting the stream...")
        >>> await asyncio.sleep(5)
        >>>
        >>> subscribed_streams = []
        >>>
        >>> for wica_stream in streams:
        >>>     print(f"Subscribing to stream {wica_stream.id}")
        >>>     subscribed_streams.append(wica_stream.subscribe())
        ```

        See examples for more detail!


        Retruns:
            int: The ID of the created stream

        """
        channels_payload = []
        if self.channels:
            for channel in self.channels:
                if channel.properties:
                    channels_payload.append(
                        {"name": channel.name, "props": channel.properties.__dict__}
                    )
                else:
                    channels_payload.append({"name": channel.name})

        if self.stream_properties:
            payload = {"channels": channels_payload, "props": WicaStreamProperties}
        else:
            payload = {"channels": channels_payload}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url=self.base_url, json=payload)
                if response.is_success:
                    self.id = int(response.json())
                    self._logger.debug(
                        f"successfully started stream with id: {self.id}"
                    )
                    return self.id
                else:
                    response.raise_for_status()

            except httpx.RequestError as exc:
                self._logger.debug(
                    f"A RequestError occurred while creating stream {exc.request.url!r}."
                )
                raise StreamNotCreatedException(
                    "A RequestError occurred while creating stream {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                self._logger.debug(
                    f"StatusError response {exc.response.status_code} while creating stream {exc.request.url!r}."
                )
                raise StreamNotCreatedException(
                    "StatusError response while creating stream {exc.request.url!r}."
                )

    async def subscribe(self) -> AsyncIterator[WicaMessage]:
        """Subscribe to a stream.

        If the stream doesn't exists this function will call create() to create a new stream.


        Yields:
            AsyncIterator[WicaMessage]: That returns the messages sent by the server.
        """
        if not self.id:
            try:
                self._logger.debug("Trying to create stream")
                await self.create()
            except (StreamNotCreatedException):
                self._logger.debug("Couldn't create stream")

        async with httpx.AsyncClient() as client:
            # Compiling regex for segmenting the messages returned by the client
            regex_event = re.compile(r"(?<=\-)(\w+)$")
            regex_value_type = re.compile(r"(?<=\w\s)([a-z]+)")
            regex_time = re.compile(r"(.*)(?=\s\-\s\w)")
            wica_client = None
            try:
                # get the stream
                async with client.stream(
                    "GET", url=self.base_url + f"/{self.id}"
                ) as response:
                    if response.is_success:
                        wica_client = WicaSSEClient(response.aiter_bytes())
                        async for event in wica_client.events():
                            message = WicaMessage()
                            message.stream_id = int(event.id)
                            message.event = re.search(regex_event, event.event).group(0)
                            message.value_type = re.search(
                                regex_value_type, event.msg_info
                            ).group(0)
                            message.data = (
                                event.data
                                if message.event == "heartbeat"
                                else json.loads(event.data)
                            )
                            message.time = re.search(regex_time, event.msg_info).group(
                                0
                            )
                            yield message
                    else:
                        response.raise_for_status()

            except httpx.RequestError as exc:
                self._logger.debug(
                    f"A RequestError error occurred while subscribing to the stream {exc.request.url!r}."
                )
                raise StreamSubscriptionException(
                    f"A RequestError error occurred while subscribing to the stream  {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                self._logger.debug(
                    f"StatusError response {exc.response.status_code} while subscribing to the stream  {exc.request.url!r}."
                )
                raise StreamSubscriptionException(
                    f"A StatusError occurred while subscribing to the stream  {exc.request.url!r}."
                )
            finally:
                if wica_client:
                    await wica_client.close()

    async def destroy(self) -> httpx.Response:
        """Destroys the stream on the server.

        This method sends a delete request to the server and thereby destroys the stream.
        This is also the best way to stop a running subscription.

        Returns:
            Response: Returns the http response
        """
        async with httpx.AsyncClient() as client:
            try:
                if not self.id:
                    self._logger.debug(
                        "Stream was no deleted because no ID was provided!"
                    )
                    raise StreamNotDeletedException(
                        "Stream was not deleted because no ID was provided!"
                    )
                response = await client.delete(url=self.base_url + f"/{self.id}")
                if response.is_success:
                    return response
                else:
                    response.raise_for_status()
            except httpx.RequestError as exc:
                self._logger.debug(
                    f"A RequestError occurred while deleting stream  {exc.request.url!r}."
                )
                raise StreamNotDeletedException(
                    f"A RequestError occurred while deleting stream {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                self._logger.debug(
                    f"StatusError response {exc.response.status_code} while deleting stream  {exc.request.url!r}."
                )
                raise StreamNotDeletedException(
                    f"StatusError response {exc.response.status_code} while deleting stream  {exc.request.url!r}."
                )
