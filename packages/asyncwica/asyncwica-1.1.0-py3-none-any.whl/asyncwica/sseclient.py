"""Server Side Events (SSE) client for Wica.

Provides a generator of SSE received through an existing HTTP response.
"""

import logging

_FIELD_SEPARATOR = ":"


class WicaSSEClient(object):
    def __init__(self, event_source, char_enc="utf-8"):
        """Initialize the SSE client over an existing, ready to consume event source.

        The event source is expected to be a binary stream and have a aclose()
        method. Currently this has only been tested with httpx.
        """
        self._logger = logging.getLogger(self.__class__.__module__)
        self._logger.debug("Initialized SSE client from event source %s", event_source)
        self._event_source = event_source
        self._char_enc = char_enc

    async def _read(self):
        """Read the incoming event source stream and yield event chunks.

        Unfortunately it is possible for some servers to decide to break an
        event into multiple HTTP chunks in the response. It is thus necessary
        to correctly stitch together consecutive response chunks and find the
        SSE delimiter (empty new line) to yield full, correct event chunks.
        """
        data = b""
        async for chunk in self._event_source:
            for line in chunk.splitlines(True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    async def events(self):
        async for chunk in self._read():
            event = Event()
            # Split before decoding so splitlines() only uses \r and \n
            for line in chunk.splitlines():
                # Decode the line.
                line = line.decode(self._char_enc)

                # Lines starting with a separator are comments and are to be
                # ignored.
                if not line.strip():
                    continue

                data = line.split(_FIELD_SEPARATOR, 1)
                field = data[0]

                # This is the wica specifi part:
                # Catch any field without name, thats the message info.
                # We implement that by changing the value of field to 'msg_info'
                if field == "":
                    field = "msg_info"
                # Ignore unknown fields.
                if field not in event.__dict__:
                    self._logger.debug(
                        "Saw invalid field %s while parsing " "Server Side Event", field
                    )
                    continue

                if len(data) > 1:
                    # From the spec:
                    # "If value starts with a single U+0020 SPACE character,
                    # remove it from value."
                    if data[1].startswith(" "):
                        value = data[1][1:]
                    else:
                        value = data[1]
                else:
                    # If no value is present after the separator,
                    # assume an empty value.
                    value = ""

                # The data field may come over multiple lines and their values
                # are concatenated with each other.
                if field == "data":
                    event.__dict__[field] += value + "\n"
                else:
                    event.__dict__[field] = value

            # Events with no data are not dispatched.
            if not event.data:
                continue

            # If the data field ends with a newline, remove it.
            if event.data.endswith("\n"):
                event.data = event.data[0:-1]

            # Empty event names default to 'message'
            event.event = event.event or "message"

            # Dispatch the event
            self._logger.debug("Dispatching %s...", event)
            yield event

    async def close(self):
        """Manually close the event source stream."""
        await self._event_source.aclose()


class Event(object):
    """Representation of an event from the event stream."""

    def __init__(
        self,
        id: int = None,
        event: str = "message",
        data: str = "",
        msg_info: str = "",
        retry=None,
    ):
        self.id = id
        self.event = event
        self.data = data
        self.msg_info = msg_info
        self.retry = retry

    def __str__(self):
        s = "{0} event".format(self.event)
        if self.id:
            s += " #{0}".format(self.id)
        if self.data:
            s += ", {0} byte{1}".format(len(self.data), "s" if len(self.data) else "")
        else:
            s += ", no data"
        if self.msg_info:
            s += ", message info: {0} ".format(self.msg_info)
        if self.retry:
            s += ", retry in {0}ms".format(self.retry)
        return s
