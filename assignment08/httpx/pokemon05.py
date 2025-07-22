import asyncio          # ใช้สำหรับ async/await
import httpx            # ไลบรารีสำหรับส่ง HTTP request แบบ async
import time             # ใช้จับเวลา

# รายชื่อโปเกม่อนที่จะดึงข้อมูล
pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

# list กลางสำหรับเก็บข้อมูลโปเกม่อนทั้งหมด
pokemon_data_list = []

# ฟังก์ชันดึงข้อมูลของโปเกม่อนแต่ละตัว
async def fetch_pokemon_data(name, client):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = await client.get(url)
    data = response.json()

    # สกัดเฉพาะข้อมูลที่ต้องการ
    pokemon_data = {
        "name": data["name"].title(),          # ชื่อโปเกม่อนแบบมีอักษรตัวใหญ่ขึ้นต้น
        "id": data["id"],                      # รหัสประจำโปเกม่อน
        "base_xp": data["base_experience"]     # ค่าประสบการณ์พื้นฐาน
    }

    # เก็บลง list กลาง
    pokemon_data_list.append(pokemon_data)

# ฟังก์ชันสำหรับใช้กับ sorted (แทน lambda)
def sort_by_base_xp(pokemon):
    return pokemon["base_xp"]

# ฟังก์ชันหลัก
async def main():
    start = time.time()  # เริ่มจับเวลา

    async with httpx.AsyncClient() as client:
        # สร้าง tasks สำหรับ fetch ข้อมูลแต่ละตัว
        tasks = [fetch_pokemon_data(name, client) for name in pokemon_names]
        await asyncio.gather(*tasks)  # รอให้ tasks ทุกตัวเสร็จพร้อมกัน

    # เรียงลำดับตาม base_xp (น้อย → มาก)
    sorted_pokemon = sorted(pokemon_data_list, key=sort_by_base_xp, reverse=False)

    # แสดงผลลัพธ์
    print("=== รายชื่อโปเกม่อน (เรียงตาม Base XP มาก -> น้อย) ===")
    for p in sorted_pokemon:
        print(f"{p['name']:<12} -> ID: {p['id']:<4} Base XP: {p['base_xp']}")

    # แสดงเวลา
    end = time.time()
    print("ใช้เวลา:", round(end - start, 2), "วินาที")

# เรียกใช้ main() แบบ async เมื่อรัน script นี้โดยตรง
if __name__ == "__main__":
    asyncio.run(main())
