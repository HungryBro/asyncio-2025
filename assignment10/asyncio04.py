import asyncio
from datetime import datetime

# helper แสดงเวลาแบบสวย ๆ
def ts() -> str:
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

# ----- Producer: ลูกค้าใส่ออเดอร์ลงคิว -----
async def customer(name: str, items: list[str], q: asyncio.Queue):
    print(f"[{ts()}] ({name}) finished shopping: {items}")
    await q.put((name, items))  # 1 ออเดอร์ = 1 งานบนคิว

# ----- Consumer: แคชเชียร์ดึงออเดอร์จากคิวมาคิดเงิน -----
async def cashier(cid: int, per_item_sec: float, q: asyncio.Queue):
    try:
        while True:
            name, items = await q.get()       # รับ 1 งาน
            print(f"[{ts()}] [Cashier-{cid}] processing {name} with orders {items}")
            for _ in items:                    # คิดเงินทีละชิ้น
                await asyncio.sleep(per_item_sec)
            print(f"[{ts()}] [Cashier-{cid}] finished {name}")
            q.task_done()                      # งานนี้เสร็จแล้ว
    except asyncio.CancelledError:
        print(f"[{ts()}] [Cashier-{cid}] closed")
        raise

# ----- Main -----
async def main():
    q = asyncio.Queue()

    # สร้างแคชเชียร์ (Consumer) 2 คน: คนแรก 1 วิ/ชิ้น, คนสอง 2 วิ/ชิ้น
    c1 = asyncio.create_task(cashier(1, 1, q))
    c2 = asyncio.create_task(cashier(2, 2, q))

    # รายชื่อลูกค้า (Producer)
    jobs = [
        customer("Alice",   ["Apple", "Banana", "Milk"], q),
        customer("Bob",     ["Bread", "Cheese"],         q),
        customer("Charlie", ["Eggs", "Juice", "Butter"], q),
    ]
    await asyncio.gather(*jobs)   # ทุกคนช้อปเสร็จและโยนออเดอร์ลงคิว

    await q.join()                # รอให้ทุกงานบนคิวถูกคิดเงินครบ

    # ปิดเคาน์เตอร์อย่างปลอดภัย (ยกเลิกลูปรอคิว)
    for t in (c1, c2):
        t.cancel()
    await asyncio.gather(c1, c2, return_exceptions=True)

    print(f"[{ts()}] [Main] Supermarket closed!")

if __name__ == "__main__":
    asyncio.run(main())
