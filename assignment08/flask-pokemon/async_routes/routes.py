import time
import requests
import random
from flask import Blueprint, render_template, current_app
import httpx, asyncio
# Create a Blueprint for sync routes
async_bp = Blueprint("async", __name__)

# ดึงข้อมูลโปเกม่อนจาก URL
async def get_pokemon(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"{time.ctime()} - get {url}")
    return response.json()

# ดึงข้อมูลโปเกม่อนหลายตัว
async def get_pokemons():
    # Get the number of comics to fetch from app config
    NUMBER_OF_POKEMON = current_app.config["NUMBER_OF_XKCD"]

    # Generate a list of random comic numbers (0–300)
    rand_list=[]
    for i in range(NUMBER_OF_POKEMON):
        rand_list.append(random.randint(0,300))

    pokemon_data = []
    for number in rand_list:
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        xkcd_json = get_pokemon(url)   # Fetch comic JSON
        pokemon_data.append(xkcd_json)
    pokemon_data = await asyncio.gather(*pokemon_data)  # Gather all async calls
    return pokemon_data

# Route
@async_bp.route('/')
def home():
    start_time = time.perf_counter()
    pokemons = asyncio.run(get_pokemons())
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Get {len(pokemons)} Pokémon. Time taken: {end_time-start_time} seconds")

    return render_template('sync.html',
                           title="Pokémon Flask App",
                           heading="Pokémon Asynchronous Version",
                           pokemons=pokemons,  # ส่งไปใช้ template เดิม แต่เปลี่ยนเนื้อหา
                           end_time=end_time,
                           start_time=start_time)