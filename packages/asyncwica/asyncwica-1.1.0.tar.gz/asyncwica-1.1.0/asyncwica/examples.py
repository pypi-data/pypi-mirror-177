# import time
# import asyncio


# async def async_simple_example():
#     """A simple example of how to use AsyncWicaStream. Run it in main by uncommenting it! """

#     wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])

#     async def run_stream():
#         await wica_stream.create()
#         async for message in wica_stream.subscribe():
#             print(message)

#     async def stop_stream():
#         await asyncio.sleep(10)
#         print(await wica_stream.destroy())

#     await asyncio.gather(run_stream(), stop_stream())


# async def async_multistream_example():
#     """ An example of how to run multiple streams at once using aiostream Run it in main by uncommenting it! """
#     from aiostream import stream
#     streams = []
#     async def run_streams():
#         for _ in range(10):
#             wica_stream = AsyncWicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])
#             streams.append(wica_stream)
#             await wica_stream.create()

#         print("Doing someting else before starting the stream...")
#         await asyncio.sleep(5)

#         subscribed_streams = []

#         for wica_stream in streams:
#             print(f"Subscribing to stream {wica_stream.id}")
#             subscribed_streams.append(wica_stream.subscribe())


#         combine = stream.merge(*subscribed_streams)
#         async with combine.stream() as streamer:
#             async for item in streamer:
#                 print(item)
#                 continue


#     async def stop_streams():
#         await asyncio.sleep(25)
#         for wica_stream in streams:
#             print(await wica_stream.destroy())


#     await asyncio.gather(run_streams(), stop_streams())


# async def main():
#     #await simple_example_blocking_io()
#     #await async_simple_example()
#     #await async_multistream_example()
#     pass

# if __name__ == "__main__":
#     asyncio.run(main())
