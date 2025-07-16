import asyncio
import httpx
import time

# รายชื่อโปเกม่อน
pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

# สร้าง list เปล่าไว้เก็บข้อมูลโปเกม่อนทั้งหมด
pokemon_data_list = []

# ฟังก์ชันดึงข้อมูลโปเกม่อน
async def fetch_pokemon_data(name, client):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = await client.get(url)
    data = response.json()

    # เก็บข้อมูลในรูปแบบ dictionary
    pokemon_data = {
        "name": data["name"].title(),
        "id": data["id"],
        "base_xp": data["base_experience"]
    }

    # ใส่ข้อมูลลงใน list กลาง
    pokemon_data_list.append(pokemon_data)

# ฟังก์ชันสำหรับใช้กับ sorted (แทน lambda)
def sort_by_base_xp(pokemon):
    return pokemon["base_xp"]

# ฟังก์ชันหลัก
async def main():
    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = []
        for name in pokemon_names:
            tasks.append(fetch_pokemon_data(name, client))
        await asyncio.gather(*tasks)

    # เรียงลำดับจาก base_xp มากไปน้อย
    sorted_pokemon = sorted(pokemon_data_list, key=sort_by_base_xp, reverse=True)

    # แสดงผลลัพธ์
    print("=== รายชื่อโปเกม่อน (เรียงตาม Base XP มาก -> น้อย) ===")
    for p in sorted_pokemon:
        print(f"{p['name']:<12} -> ID: {p['id']:<4} Base XP: {p['base_xp']}")

    end = time.time()
    print("ใช้เวลา:", round(end - start, 2), "วินาที")

# เรียกใช้งาน
asyncio.run(main())
