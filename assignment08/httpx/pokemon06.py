# นำเข้า asyncio สำหรับเขียนโปรแกรมแบบ asynchronous
import asyncio

# นำเข้า httpx สำหรับการส่ง HTTP requests แบบ async
import httpx

# URL สำหรับดึงรายการ abilities ทั้งหมด (กำหนด limit = 20)
ABILITY_LIST_URL = "https://pokeapi.co/api/v2/ability/?limit=20"

# ฟังก์ชันช่วยในการนับจำนวนโปเกม่อนที่ใช้ ability นี้
def count_pokemon_in_ability(data):
    name = data["name"]                  # ชื่อของ ability
    pokemon_list = data["pokemon"]       # รายการโปเกม่อนทั้งหมดที่ใช้ ability นี้
    return name, len(pokemon_list)       # คืนชื่อ และ จำนวนโปเกม่อน

# ฟังก์ชัน async สำหรับดึงรายละเอียด ability จากลิงก์
async def fetch_ability_detail(url, client):
    response = await client.get(url)     # ดึงข้อมูลจาก URL
    return response.json()               # คืนข้อมูลในรูปแบบ JSON (dict)

# ฟังก์ชันหลักของโปรแกรม
async def main():
    async with httpx.AsyncClient() as client:
        # ดึงรายการ ability หลัก (เช่น stench, drizzle, speed-boost ...)
        response = await client.get(ABILITY_LIST_URL)

        # ดึงเฉพาะ 10 รายการแรก
        abilities = response.json()["results"][:10]

        # สร้าง task สำหรับดึงข้อมูลรายละเอียดของแต่ละ ability
        tasks = []
        for item in abilities:
            url = item["url"]                # ลิงก์ไปยังข้อมูลแต่ละ ability
            tasks.append(fetch_ability_detail(url, client))  # สร้าง task

        # เรียกใช้งาน tasks ทั้งหมดพร้อมกัน
        ability_details = await asyncio.gather(*tasks)

        # วนลูปเพื่อแสดงผลข้อมูล
        for detail in ability_details:
            name, count = count_pokemon_in_ability(detail)
            print(f"{name:<20} → {count} Pokémon")

# รันโปรแกรม ถ้าถูกเรียกตรงจาก __main__
if __name__ == "__main__":
    asyncio.run(main())
