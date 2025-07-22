# นำเข้าโมดูล asyncio สำหรับเขียนโปรแกรมแบบ asynchronous
import asyncio

# นำเข้าไลบรารี httpx ที่ใช้สำหรับส่ง HTTP request แบบ asynchronous
import httpx

# กำหนดฟังก์ชันหลักแบบ async ชื่อว่า main
async def main():
    # สร้าง httpx.AsyncClient() ซึ่งเป็น client ที่ใช้ส่ง HTTP request แบบ async
    # ใช้ with เพื่อให้ client ปิดตัวเองเมื่อเสร็จการใช้งาน (context manager)
    async with httpx.AsyncClient() as client:
        # ใช้ await เพื่อรอผลลัพธ์จากการส่ง GET request ไปยัง 'https://www.example.com'
        response = await client.get('https://www.example.com')

        # แสดง status code ของ response ที่ได้ เช่น 200 (OK), 404 (Not Found), 500 (Server Error) เป็นต้น
        print(response.status_code)

        # แสดงข้อความเนื้อหาที่ได้รับจาก server โดยตัดมาแค่ 100 ตัวอักษรแรกเพื่อความกระชับ
        print(response.text[:100])

# ใช้ asyncio.run() เพื่อรันฟังก์ชัน main() แบบ asynchronous
# ตัวนี้จะสร้าง event loop และจัดการรันโค้ด async ให้เองอัตโนมัติ
asyncio.run(main())
