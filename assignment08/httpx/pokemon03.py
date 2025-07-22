# นำเข้า asyncio สำหรับการเขียนโปรแกรมแบบ asynchronous
import asyncio

# นำเข้า httpx สำหรับส่ง HTTP request แบบ async
import httpx

# นำเข้า time สำหรับจับเวลาการประมวลผล
import time

# รายชื่อโปเกม่อนที่ต้องการดึงข้อมูล
pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

# สร้าง list เปล่าสำหรับเก็บข้อมูลโปเกม่อนหลังดึงมาครบ
pokemon_data_list = []

# ฟังก์ชัน async สำหรับดึงข้อมูลโปเกม่อนแต่ละตัว
async def fetch_pokemon_data(name, client):
    # สร้าง URL จากชื่อโปเกม่อน
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    # ส่ง HTTP GET request แบบ async และรอผลลัพธ์
    response = await client.get(url)

    # แปลง response เป็น JSON (dict) แบบ async
    data = response.json()  # ไม่มี await ได้เพราะ httpx คืน dict เลย

    # เก็บข้อมูลที่ต้องการในรูปแบบ dictionary
    pokemon_data = {
        "name": data["name"].title(),       # แปลงชื่อให้ขึ้นต้นด้วยตัวใหญ่
        "id": data["id"],                   # ID ของโปเกม่อน
        "base_xp": data["base_experience"]  # Base XP (ค่าประสบการณ์พื้นฐาน)
    }

    # เพิ่มข้อมูลนี้เข้า list กลาง
    pokemon_data_list.append(pokemon_data)

# ฟังก์ชันช่วยสำหรับใช้ในการเรียงลำดับ (แทน lambda)
def sort_by_base_xp(pokemon):
    return pokemon["base_xp"]  # คืนค่า base_xp สำหรับใช้เรียง

# ฟังก์ชันหลักของโปรแกรม
async def main():
    # เริ่มจับเวลา
    start = time.time()

    # สร้าง AsyncClient สำหรับใช้ส่ง HTTP requests
    async with httpx.AsyncClient() as client:
        tasks = []  # เก็บรายการ tasks ทั้งหมด
        for name in pokemon_names:
            # เพิ่ม task สำหรับดึงข้อมูลแต่ละตัวเข้า list
            tasks.append(fetch_pokemon_data(name, client))

        # ใช้ asyncio.gather เพื่อรัน tasks ทั้งหมดพร้อมกันแบบ async
        await asyncio.gather(*tasks)

    # เรียงลำดับจาก base_xp มากไปน้อย
    sorted_pokemon = sorted(pokemon_data_list, key=sort_by_base_xp, reverse=True)

    # แสดงผลลัพธ์แบบจัดเรียง
    print("=== รายชื่อโปเกม่อน (เรียงตาม Base XP มาก -> น้อย) ===")
    for p in sorted_pokemon:
        print(f"{p['name']:<12} -> ID: {p['id']:<4} Base XP: {p['base_xp']}")

    # จับเวลาหลังจบ
    end = time.time()
    print("ใช้เวลา:", round(end - start, 2), "วินาที")

# เรียกใช้ main() ผ่าน asyncio
asyncio.run(main())
