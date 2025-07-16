import asyncio
import httpx

pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

async def fetch_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return {
            "name": data["name"],
            "id": data["id"],
            "types": [t["type"]["name"] for t in data["types"]]
        }

async def main():
    tasks = [fetch_pokemon(name) for name in pokemon_names]
    results = await asyncio.gather(*tasks)

    for pokemon in results:
        print(f"{pokemon['name'].title()} → ID: {pokemon['id']}, Types: {pokemon['types']}")

if __name__ == "__main__":
    asyncio.run(main())
