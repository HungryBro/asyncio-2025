#
# ให้หาข้อผิดพลาดและแก้ไขโค้ดให้ทำงานถูกต้อง
# Result:
# Task A started
# Task B started
# Task A finished
# Task B finished
# All tasks done

import asyncio

async def task(name):
    print(f"Task {name} started")
    await asyncio.sleep(1)
    print(f"Task {name} finished")

async def main():
    t1 = asyncio.create_task(task("A"))
    t2 = asyncio.create_task(task("B"))

    await asyncio.gather(t1, t2)

    print("All tasks done")

asyncio.run(main())

