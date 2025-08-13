import asyncio, time

async def worker_ok():
    print(f"[{time.ctime():}] Worker OK is Starting")
    await asyncio.sleep(1)  # Simulate some work
    print(f"[{time.ctime():}] Worker OK completed")

async def main():
    asyncio.create_task(worker_ok()) # fire and forget
    await asyncio.sleep(2)  # Wait for the worker to finish

asyncio.run(main()) 