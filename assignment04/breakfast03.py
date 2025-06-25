# Asynchronous breakfast
import asyncio
from time import sleep, time

async def make_coffee():
    print("coffee: prepare ingridents")
    sleep(1)
    print("coffee: waiting...")
    await asyncio.sleep(5)  # async sleep
    print("coffee: ready")

async def fry_eggs():
    print("eggs: prepare ingridents")
    sleep(1)
    print("eggs: frying...")
    await asyncio.sleep(3)  # async sleep
    print("eggs: ready")

async def main():
    start = time()

    # เริ่มทั้งสอง task พร้อมกัน
    task1 = asyncio.create_task(make_coffee())
    task2 = asyncio.create_task(fry_eggs())

    await task1
    await task2

    print(f"breakfast is ready in {time() - start} min")

asyncio.run(main())  # run top-level async function
