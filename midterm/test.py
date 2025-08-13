import asyncio  # นำเข้าโมดูล asyncio สำหรับการทำงานแบบ asynchronous

async def download(file_name, size_mb, delay_sec):  # ฟังก์ชัน async สำหรับจำลองการดาวน์โหลด
    """ จำลองการดาวน์โหลดไฟล์ """  
    await asyncio.sleep(delay_sec)  # รอเวลาตาม delay_sec เพื่อจำลองการดาวน์โหลด
    speed = size_mb / delay_sec  # คำนวณความเร็วการดาวน์โหลด (MB/วินาที)
    print(f"{file_name} downloaded at {speed:.2f} MB/s")  # แสดงผลไฟล์และความเร็ว

async def main():  # ฟังก์ชันหลัก async สำหรับจัดการการดาวน์โหลด
    # สร้าง tasks สำหรับดาวน์โหลดทั้ง 3 ไฟล์
    tasks = [  # สร้างลิสต์ของ tasks
        asyncio.create_task(download("File A", 300, 3)),  # สร้าง task สำหรับ File A
        asyncio.create_task(download("File B", 200, 2)),  # สร้าง task สำหรับ File B
        asyncio.create_task(download("File C", 100, 1))   # สร้าง task สำหรับ File C
    ]
    await asyncio.gather(*tasks)  # รอให้ทุก tasks ทำงานเสร็จพร้อมกัน

asyncio.run(main())  # เริ่มต้นการทำงาน async และรันฟังก์ชัน main()