# asyncio producer–consumer (non-blocking get) demo
# เขียนให้อ่านง่าย เหมาะมือใหม่ ไม่มี lambda

import asyncio
from random import random

# ---------------- Producer ----------------
async def producer(queue: asyncio.Queue) -> None:
    print("Producer: Running")
    # สร้างงาน 10 ชิ้น
    for i in range(10):
        value = i
        # หน่วงเวลาเพื่อจำลองการทำงาน
        sleeptime = random()          # 0.0–1.0 วินาที
        print(f"> Producer {value} sleep {sleeptime:.2f}s")
        await asyncio.sleep(sleeptime)
        # ใส่งานลงคิว
        await queue.put(value)
        print(f"> Producer put {value}")

    # ส่งสัญญาณจบงาน (sentinel) ให้ผู้บริโภค
    await queue.put(None)
    print("Producer: Done")

# ---------------- Consumer ----------------
async def consumer(queue: asyncio.Queue) -> None:
    print("Consumer: Running")
    while True:
        # ดึงงานแบบไม่บล็อก (ถ้าไม่มีจะรอเองเล็กน้อย)
        try:
            item = queue.get_nowait()
        except asyncio.QueueEmpty:
            print("Consumer: got nothing, waiting a while...")
            await asyncio.sleep(0.5)  # เว้นจังหวะ ไม่ busy-wait
            continue

        # ตรวจสัญญาณหยุด
        if item is None:
            break

        # ประมวลผลงาน (ตัวอย่างนี้แค่พิมพ์)
        print(f"\t> Consumer got {item}")

    print("Consumer: Done")

# ---------------- Entry Point ----------------
async def main() -> None:
    # สร้างคิวที่ใช้ร่วมกัน
    queue: asyncio.Queue = asyncio.Queue()

    # รัน producer และ consumer พร้อมกัน
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )

if __name__ == "__main__":
    asyncio.run(main())
