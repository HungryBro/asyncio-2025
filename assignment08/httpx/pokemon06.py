import asyncio
import httpx

ABILITY_LIST_URL = "https://pokeapi.co/api/v2/ability/?limit=20"

def count_pokemon_in_ability(data):
    name = data["name"]
    pokemon_list = data["pokemon"]
    return name, len(pokemon_list)

async def fetch_ability_detail(url, client):
    response = await client.get(url)
    return response.json()

async def main():
    async with httpx.AsyncClient() as client:
        # ดึงรายการ abilities
        response = await client.get(ABILITY_LIST_URL)
        abilities = response.json()["results"][:10]

        # เตรียมลิงก์สำหรับดึงรายละเอียด
        tasks = []
        for item in abilities:
            url = item["url"]
            tasks.append(fetch_ability_detail(url, client))

        # ดึงข้อมูลพร้อมกัน
        ability_details = await asyncio.gather(*tasks)

        # แสดงผล
        for detail in ability_details:
            name, count = count_pokemon_in_ability(detail)
            print(f"{name:<20} → {count} Pokémon")

if __name__ == "__main__":
    asyncio.run(main())