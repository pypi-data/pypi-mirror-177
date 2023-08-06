# import time
# import asyncio


# async def simple_example_blocking_io():
#     """A simple example of how to use WicaStream.
#     In this example we are using asyncio, but you could use any other concurrency or parallel processing package,
#     you just need the ability to interrupt the stream somehow!
#     """

#     wica_stream = WicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])

#     def run_stream():
#         wica_stream.create()
#         for message in wica_stream.subscribe():
#             print(message)

#     def stop_stream():
#         print("Starting to wait")
#         time.sleep(5)
#         print(wica_stream.destroy())

#     # The following functions put the blocking functions into their own thread.
#     async def thread_run_stream():
#         return await asyncio.to_thread(run_stream)

#     async def thread_stop_stream():
#         return await asyncio.to_thread(stop_stream)

#     return await asyncio.gather(thread_run_stream(), thread_stop_stream())


# async def main():
#     await simple_example_blocking_io()


# if __name__ == "__main__":
#     asyncio.run(main())
