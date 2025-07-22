# นำเข้า asyncio สำหรับเขียนโปรแกรมแบบ asynchronous
import asyncio

# นำเข้า httpx สำหรับการส่ง HTTP requests แบบ async
import httpx

# รายชื่อโปเกม่อนที่ต้องการดึงข้อมูลจาก API
pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

# ฟังก์ชัน async สำหรับดึงข้อมูลโปเกม่อนจาก API
async def fetch_pokemon(name):
    # สร้าง URL ของแต่ละโปเกม่อน
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    # สร้าง client เพื่อเชื่อมต่อ API แบบ async
    async with httpx.AsyncClient() as client:
        # ส่ง HTTP GET request แบบ async
        response = await client.get(url)

        # แปลง response เป็น dict โดยไม่ต้อง await เพราะ httpx คืนมาให้เลย
        data = response.json()

        # คืนค่าข้อมูลที่เราสนใจ: ชื่อ, ID, และประเภทของโปเกม่อน
        return {
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]]
        }

# ฟังก์ชันหลักของโปรแกรม
async def main():
    # สร้าง tasks สำหรับโปเกม่อนแต่ละตัว
    tasks = [fetch_pokemon(name) for name in pokemon_names]

    # เรียกใช้งาน fetch_pokemon ทั้งหมดพร้อมกัน แล้วรอผลลัพธ์
    results = await asyncio.gather(*tasks)

    # แสดงผลลัพธ์ที่ได้ออกมา
    for pokemon in results:
        print(f"{pokemon['name'].title()} → ID: {pokemon['id']}, Types: {pokemon['types']}")

# ตรวจสอบว่า script นี้ถูกรันตรง ๆ (ไม่ใช่ถูก import จากไฟล์อื่น)
# แล้วค่อยรัน main() ผ่าน asyncio
if __name__ == "__main__":
    asyncio.run(main())
