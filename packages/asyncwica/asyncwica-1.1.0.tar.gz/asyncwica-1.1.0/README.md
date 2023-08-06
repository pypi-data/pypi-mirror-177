# PyWica - Async Wica Python API
[![pipeline status](https://git.psi.ch/proscan_data/py-wica/badges/async/pipeline.svg)](https://git.psi.ch/proscan_data/py-wica/-/commits/async)
[![coverage report](https://git.psi.ch/proscan_data/py-wica/badges/async/coverage.svg)](https://git.psi.ch/proscan_data/py-wica/-/commits/async)

#### Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick-start Guid](#quick-start-guide)
- [Documentation](#documentation)
- [Dependencies](#dependencies)
- [Contribute](#contribute)
- [Project Changes and Tagged Releases](#project-changes-and-tagged-releases)
- [Developer Notes](#developer-notes)
- [Contact](#contact)

# Introduction
This project/package aims to provide a simple python interface to the wica-http server.
Check out the main branch to get the blocking version of the package

# Installation
Install with pip
```bash
pip install asyncwica
```
# Quick-start Guide
```python
import asyncio
import time

from asyncwica import AsyncWicaStream


async def async_simple_example():
    """A simple example of how to use AsyncWicaStream. """

    wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])

    async def run_stream():
        await wica_stream.create()
        async for message in wica_stream.subscribe():
            print(message)

    async def stop_stream():
        await asyncio.sleep(10)
        print(await wica_stream.destroy())

    await asyncio.gather(run_stream(), stop_stream())


async def async_multistream_example():
    """ An example of how to run multiple streams at once.

    Use aiostream to run it! Run it by un-commenting it in main.
    """
    from aiostream import stream
    streams = []
    async def run_streams():
        for _ in range(10):
            wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])
            streams.append(wica_stream)
            await wica_stream.create()

        print("Doing someting else before starting the stream...")
        await asyncio.sleep(5)

        subscribed_streams = []

        for wica_stream in streams:
            print(f"Subscribing to stream {wica_stream.id}")
            subscribed_streams.append(wica_stream.subscribe())


        combine = stream.merge(*subscribed_streams)
        async with combine.stream() as streamer:
            async for item in streamer:
                print(item)
                continue


    async def stop_streams():
        await asyncio.sleep(25)
        for wica_stream in streams:
            print(await wica_stream.destroy())


    await asyncio.gather(run_streams(), stop_streams())


async def main():
    await async_simple_example()
    #await async_multistream_example()


if __name__ == "__main__":
    asyncio.run(main())

```

# Documentation
Current Features:
* Custom Client to handle be able to extract last line of SSE with timestamp and message type.
* Simple functions to create, delete and subscribe to streams
* Fully Async (blocking versions available in main branch)

Check out the wiki for more info!

# Dependencies
* [httpx](https://github.com/encode/httpx/)

# Contribute
To contribute, simply clone the project.
You can uses ``` pip -r requirements.txt ``` or the make file to set up the project.


# Project Changes and Tagged Releases
* See the Changelog file for further information
* Project releases are available in pypi

# Developer Notes
Currently None

# Contact
If you have any questions pleas contract 'niklas.laufkoetter@psi.ch'
