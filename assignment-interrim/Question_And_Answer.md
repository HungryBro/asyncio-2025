# Question
1. ถ้าสร้าง asyncio.create_task(*tasks) ที่ไม่มี await ที่ main() เกิดอะไรบ้าง
   1. งานจะเป็นแบบ fire‑and‑forget: ถูก schedule แล้วเริ่มวิ่งเมื่อ event loop ว่าง แต่ main() อาจจบก่อน ทำให้ loop ปิดทั้งที่งานยังไม่เสร็จ (ผลลัพธ์หาย/ถูกยกเลิก)
   2. ถ้างานใด error จะขึ้นคำเตือน “Task exception was never retrieved” เพราะไม่มีใครไปรับ exception จาก task นั้น
   3. วิธีแก้: เก็บ reference ของ tasks แล้ว await ทีหลัง/ใช้ asyncio.gather() หรือถ้าจำเป็นต้องปล่อยจริง ๆ ให้ผูก task.add_done_callback() เพื่อบันทึกผลและจับ error
2. ความแตกต่างระหว่าง asyncio.gather(*tasks) กับ asyncio.wait(tasks) คืออะไร
   1. gather รันพร้อมกันและคืนค่าเป็น ลิสต์ผลลัพธ์ตามลำดับ args เมื่อ await กลุ่มนั้นเสร็จทุกตัว 
   2. gather (ค่าเริ่มต้น) ถ้างานใดพัง จะยกเลิกที่เหลือและ raise ทันที; หรือกำหนด retur n_exceptions=True เพื่อรวบ error กลับมาในลิสต์ได้
   3. ต้อง “แสดงผลทันทีที่เสร็จทีละตัว”: ใช้ wait(..., return_when=FIRST_COMPLETED) เพื่อสตรีมค่าที่เสร็จก่อนแบบ real‑time ตามตัวอย่าง iot-wait.py
3. สร้าง create_task() และ coroutine ของ http ให้อะไรต่างกัน
   1. create_task(coro) ห่อ coroutine เป็น Task และให้ event loop รัน พร้อมกับงานอื่น ได้ทันที (เหมาะยิง HTTP หลาย ๆ รายการพร้อมกัน)
   2. Task มีเมธอดตรวจสถานะ/ยกเลิก/ดึงผลภายหลังได้ (result(), exception(), cancel()), เหมาะกับงาน HTTP ที่อยากควบคุมรายคำขอ
   3. สร้างหลายคำขอด้วย create_task() แล้วรอด้วย asyncio.gather() เมื่อต้อง “รอครบทุก API ก่อนสรุป” (โทนเดียวกับ iot-gather.py) หรือใช้ wait(...FIRST_COMPLETED) ถ้าจะ “อัปเดตหน้าจอทันทีที่คำขอใดเสร็จ” (โทนเดียวกับ iot-wait.py)

   