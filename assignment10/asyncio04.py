# ================= Supermarket Simulation (asyncio + Queue) =================
# โจทย์: ลูกค้า (Producer) 3 คน โยน "ออเดอร์" ลงคิว แคชเชียร์ (Consumer) 2 คนดึงไปคิดเงิน
# จุดสำคัญ:
#   - ใช้ asyncio.Queue เป็น buffer คั่นกลาง (decouple) ระหว่าง producer และ consumer
#   - ใช้ queue.task_done() หนึ่งครั้งต่อหนึ่งงานที่ q.get() มา (ไม่ใช่ต่อสินค้าแต่ละชิ้น)
#   - ใช้ queue.join() เพื่อรอให้ "ทุกงาน" ถูกทำเสร็จ ก่อนจะปิดระบบอย่างปลอดภัย
#   - ยกเลิก (cancel) ลูปของแคชเชียร์หลังคิวว่าง เพื่อให้จบโปรแกรมและพิมพ์ข้อความ closed

import asyncio
from datetime import datetime
from collections import Counter

# ----- ฟังก์ชันช่วยพิมพ์เวลาในบรรทัด log -----
def ts() -> str:
    """
    คืนสตริงเวลาปัจจุบัน เช่น 'Tue Aug 26 22:14:25 2025'
    """
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

# === [เพิ่ม] ตัวจับเวลาสัมพัทธ์ (วินาทีจากตอนเริ่มโปรแกรม) ===
def make_timer():
    start = datetime.now()
    return lambda: (datetime.now() - start).total_seconds()

# ----- Producer: ลูกค้าแต่ละคนจะ "ใส่ออเดอร์" ของตนเองลงคิว -----
async def customer(name: str, items: list[str], q: asyncio.Queue, now=None):
    # แจ้งว่า “ช้อปเสร็จแล้ว” (ในโจทย์คือ finished shopping)
    print(f"[{ts()}] ({name}) finished shopping: {items}")
    # โยนงานหนึ่งชิ้นลงคิว: โครงสร้างงาน = (ชื่อลูกค้า, รายการสินค้า, เวลาเข้าแถว)
    # หมายเหตุ: 1 งาน = ลูกค้า 1 คน ไม่ใช่ 1 ชิ้นของสินค้า
    queued_at = now() if now else 0.0
    await q.put((name, items, queued_at))

# ----- Consumer: แคชเชียร์จะดึงงานจากคิวมาคิดเงินทีละงาน -----
async def cashier(cid: int, per_item_sec: float, q: asyncio.Queue, now=None, service_log=None):
    """
    cid           : หมายเลขแคชเชียร์ (เช่น 1 หรือ 2) เพื่อให้ log อ่านง่าย
    per_item_sec  : เวลา/ชิ้น (วินาที) ของแคชเชียร์คนนั้น ๆ
    q             : asyncio.Queue ที่รับงานจากลูกค้า
    now           : ฟังก์ชันคืนเวลาสัมพัทธ์ (วินาที)
    service_log   : ลิสต์สำหรับบันทึกผล (เริ่มกี่วิ, เสร็จกี่วิ, ใครคิดเงิน, เหตุผล)
    """
    try:
        # ใช้ลูปไม่รู้จบเพื่อคอยดึงงานจากคิวเรื่อย ๆ
        while True:
            # รอจนกว่าจะมีงาน (blocking แบบ async): ได้ (name, items, queued_at)
            name, items, queued_at = await q.get()

            started_at = now() if now else 0.0  # === [เพิ่ม] เวลาเริ่มคิดเงิน
            # แจ้งเริ่มประมวลผลลูกค้าคนนี้
            print(f"[{ts()}] [Cashier-{cid}] processing {name} with orders {items}")

            # คิดเงินทีละ "ชิ้น" ตาม per_item_sec
            for _ in items:
                # จำลองเวลาคิดเงินต่อชิ้น (ไม่บล็อก event loop ตัวอื่น ๆ)
                await asyncio.sleep(per_item_sec)

            # เสร็จงานของลูกค้าคนนี้
            finished_at = now() if now else 0.0  # === [เพิ่ม] เวลาเสร็จ
            print(f"[{ts()}] [Cashier-{cid}] finished {name}")

            # === [เพิ่ม] บันทึกสรุปเหตุผลว่าทำไมเป็นแคชเชียร์นี้ (ใครว่างก่อนก็ get() ได้ก่อน → FIFO)
            if service_log is not None:
                n_items = len(items)
                service_log.append({
                    "customer": name,
                    "cashier": cid,
                    "n_items": n_items,
                    "queued_at_sec": round(queued_at, 2),
                    "started_at_sec": round(started_at, 2),
                    "finished_at_sec": round(finished_at, 2),
                    "reason": (
                        f"Cashier-{cid} became available at {started_at:.2f}s "
                        f"and claimed the next job from the queue (FIFO). "
                        f"Service time = {n_items} items × {per_item_sec:.0f}s = {n_items*per_item_sec:.0f}s."
                    ),
                })

            # แจ้งคิวว่า "งานที่ดึงมาก่อนหน้าเสร็จแล้ว 1 งาน"
            q.task_done()
            # หมายเหตุ: ต้องเรียก task_done() ให้ครบทุกครั้งที่ q.get() สำเร็จ
            # มิฉะนั้น q.join() จะรอตลอดไป (deadlock)
    except asyncio.CancelledError:
        # เมื่อ main() ยกเลิก task นี้ (เพื่อปิดร้าน) จะวิ่งมาที่นี่
        print(f"[{ts()}] [Cashier-{cid}] closed")
        # ส่งต่อ exception เพื่อให้ asyncio รับรู้ว่า task ถูกยกเลิกจริง
        raise

# ----- main: ประกอบชิ้นส่วนทั้งหมดเข้าด้วยกัน -----
async def main():
    # สร้างคิวเปล่า ๆ สำหรับเก็บ "งาน" (ออเดอร์ของลูกค้า)
    q = asyncio.Queue(maxsize=3)  # (คงไว้ตามที่คุณตั้ง)
    now = make_timer()            # === [เพิ่ม] ตัวจับเวลาสัมพัทธ์
    service_log = []              # === [เพิ่ม] เก็บบันทึกเวลาทั้งหมด

    # สร้างแคชเชียร์ (consumer) 2 คน:
    #   - Cashier-1 ใช้เวลา 1 วินาที/ชิ้น
    #   - Cashier-2 ใช้เวลา 2 วินาที/ชิ้น
    c1 = asyncio.create_task(cashier(1, 1, q, now, service_log))
    c2 = asyncio.create_task(cashier(2, 2, q, now, service_log))

    # สร้างลูกค้า (producer) 10 คน (เหมือนเดิม)
    producers = [
        customer("Alice",   ["Apple", "Banana", "Milk"], q, now),
        customer("Bob",     ["Bread", "Cheese"],         q, now),
        customer("Charlie", ["Eggs", "Juice", "Butter"], q, now),
        customer("David",   ["Orange", "Yogurt"],        q, now),
        customer("Eve",     ["Tomato", "Cucumber"],      q, now),
        customer("Frank",   ["Chicken", "Rice"],         q, now),
        customer("Grace",   ["Fish", "Lemon"],           q, now),   # ← คนที่ 7
        customer("Heidi",   ["Pasta", "Sauce"],          q, now),
        customer("Ivan",    ["Coffee", "Sugar"],         q, now),
        customer("Judy",    ["Tea", "Honey"],            q, now),
    ]

    # ปล่อยให้ลูกค้าทุกคน “ช้อปเสร็จและส่งงานเข้าคิว” ให้ครบ
    await asyncio.gather(*producers)

    # รอให้ "ทุกงานบนคิว" ถูกทำเสร็จ (คือทุกลูกค้าถูกคิดเงินครบ)
    await q.join()

    # เมื่อคิวว่างและงานเสร็จหมดแล้ว → สั่งปิดเคาน์เตอร์:
    c1.cancel()
    c2.cancel()
    await asyncio.gather(c1, c2, return_exceptions=True)

    # ปิดร้าน (log สุดท้าย)
    print(f"[{ts()}] [Main] Supermarket closed!")

    # ================= [เพิ่ม] รายงานผล =================
    # เรียงตามเวลาที่เริ่มถูกคิดเงิน
    service_log.sort(key=lambda r: r["started_at_sec"])
    print("\n=== Processing Timeline (relative seconds) ===")
    for r in service_log:
        print(f"{r['customer']:>10} | start {r['started_at_sec']:6.2f}s | "
              f"finish {r['finished_at_sec']:6.2f}s | cashier {r['cashier']} | items={r['n_items']}")

    # รายงาน "คนที่ 7" (Grace)
    target = next((r for r in service_log if r["customer"] == "Grace"), None)
    if target:
        print(f"\n>>> คนที่ 7 (Grace) เริ่มคิดเงินที่ {target['started_at_sec']:.2f}s "
              f"เสร็จที่ {target['finished_at_sec']:.2f}s โดย Cashier-{target['cashier']}")
        print(f"เหตุผล: {target['reason']}")

    # === [เพิ่ม] รายงานจำนวนลูกค้าต่อแคชเชียร์ ===
    cashier_counts = Counter(r["cashier"] for r in service_log)
    print("\n=== Number of customers served by each cashier ===")
    for cid in sorted(cashier_counts):
        print(f"Cashier-{cid}: {cashier_counts[cid]} customers")

# จุดเริ่มโปรแกรม: รัน event loop และเรียก main()
if __name__ == "__main__":
    asyncio.run(main())

# -------------------------- หมายเหตุเพิ่มเติม --------------------------

# 1) โค้ดหลักเหมือนเดิม เพิ่มเฉพาะ: ตัวนับเวลา now(), service_log, และพิมพ์รายงานท้ายสุด
# 2) ทำไม “เป็นแคชเชียร์คนนั้น”: เพราะใคร “ว่างก่อน” ก็ await q.get() ได้ก่อน → หยิบงานถัดไปตาม FIFO
# 3) ด้วยพารามิเตอร์นี้ (Cashier-1 = 1 วิ/ชิ้น, Cashier-2 = 2 วิ/ชิ้น)
#    ลำดับโดยประมาณจะเป็น: (C1) Alice→Charlie→Eve→... และ (C2) Bob→David→...
#    เมื่อถึงคิว Frank (6) และ Grace (7) ใกล้ ๆ t≈8s แคชเชียร์ทั้งสองมักจะว่างพร้อมกัน
#    → ใครชิง q.get() ก่อน จะได้ Frank, อีกคนจะได้ Grace (ทั้งคู่เริ่ม ~8s)
#    ดังนั้น Grace มักจะไปอยู่ที่ Cashier-2 และเริ่ม ~8s (จบ ~12s) แต่เวลาจริงอาจคลาดเคลื่อนเล็กน้อยตามการสลับของ event loop
