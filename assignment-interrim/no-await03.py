import asyncio, time

async def worker_long():
    print (f"[{time.ctime():}] Worker Long is Starting")
    try:
        await asyncio.sleep(5)  # Simulate some long work
        print(f"[{time.ctime():}] Worker Long done")
    except asyncio.CancelledError:
        print(f"[{time.ctime():}] Worker Long was cancelled")

async def main():
    print(f"[{time.ctime():}] Starting main loop...")
    asyncio.create_task(worker_long())  # fire and forget
    await asyncio.sleep(1) # main loop fishes before worker_long()
    print(f"[{time.ctime():}] Main loop finished....!")

asyncio.run(main()) 