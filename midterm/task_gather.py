import asyncio
import time

async def work(i):
    print(f"[{time.time():.2f}] Starting work {i}")
    await asyncio.sleep(1) 
    print(f"[{time.time():.2f}] Done work {i}")
    return i

async def main():
    print(f"[{time.time():.2f}] Creating tasks...")
    tasks = [asyncio.create_task(work(i)) for i in range(3)]

    print(f"[{time.time():.2f}] Tasks created, waiting gather...")
    await asyncio.gather(*tasks)
    print(f"[{time.time():.2f}] All tasks completed.")

asyncio.run(main())