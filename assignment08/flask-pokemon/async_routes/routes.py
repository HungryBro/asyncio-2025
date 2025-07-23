import time
import random
import asyncio
import httpx
from flask import Blueprint, render_template, current_app

# Create a Blueprint for async routes
async_bp = Blueprint("async", __name__)

# Async helper function to fetch a single XKCD JSON by URL
async def fetch_pokemon(client, url):
    response = await client.get(url)
    print(f"{time.ctime()} - get {url}")
    return response.json()



# Async helper function to fetch multiple XKCD comics
async def get_pokemons():
    NUMBER = current_app.config["NUMBER_OF_POKEMON"]
    rand_list = [random.randint(1, 1000) for _ in range(NUMBER)]

    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, f"https://pokeapi.co/api/v2/pokemon/{number}") for number in rand_list]
        return await asyncio.gather(*tasks) 
    

# Async route: GET /async/
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    pokemons = await get_pokemons()
    end_time = time.perf_counter()


    return render_template('async.html'
                           , title="Pokemon Flask Application"
                           , heading="Pokemon Flask Version"
                           , pokemons=pokemons
                           , end_time=end_time
                           , start_time=start_time)