# นำเข้า asyncio สำหรับจัดการกับ asynchronous functions
import asyncio

# นำเข้า httpx ซึ่งเป็นไลบรารีที่ใช้ส่ง HTTP requests แบบ asynchronous
import httpx

# ฟังก์ชัน fetch() ทำหน้าที่ส่ง HTTP GET request ไปยัง URL ที่ระบุ
# ฟังก์ชันนี้เป็น async ต้องใช้ await ในการเรียกใช้
async def fetch(url):
    # สร้าง AsyncClient สำหรับส่ง request แบบ async โดยใช้ context manager
    async with httpx.AsyncClient() as client:
        # ส่ง HTTP GET request ไปยัง url ที่กำหนด แล้วรอรับผลลัพธ์ด้วย await
        response = await client.get(url)
        # คืนค่าเป็น tuple ประกอบด้วย url และ status code ของ response
        return url, response.status_code

# ฟังก์ชันหลัก ที่จะถูกรันโดย asyncio
async def main():
    # สร้างรายการ URL ที่จะส่ง request ไปหา
    urls = [
        'https://example.com',
        'https://httpbin.org/get',
        'https://api.github.com',
    ]

    # สร้างรายการของ tasks โดยการเรียก fetch(url) สำหรับแต่ละ URL ในลิสต์
    # tasks จะเป็นรายการของ coroutine objects ที่ยังไม่ถูกรัน
    tasks = [fetch(url) for url in urls]

    # ใช้ asyncio.gather เพื่อรัน tasks ทั้งหมดพร้อมกันแบบ async
    # โดยรอให้ทุก task เสร็จแล้วรวบรวมผลลัพธ์เป็นลิสต์ของ tuple
    results = await asyncio.gather(*tasks)

    # วนลูปแสดงผล URL และ Status Code ที่ได้จากแต่ละ request
    for url, status in results:
        print(f'URL: {url} → Status Code: {status}')

# เรียกใช้ main() โดยใช้ asyncio.run ซึ่งจะสร้าง event loop และรันโค้ด async ให้
asyncio.run(main())
