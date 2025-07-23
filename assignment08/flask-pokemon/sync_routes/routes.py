import time
import random
import httpx
from flask import Blueprint, render_template, current_app

sync_bp = Blueprint("sync", __name__)

def get_pokemon(url):
    with httpx.Client() as client:
        response = client.get(url)
        print(f"{time.ctime()} - get {url}")
        return response.json()

def get_pokemons():
    NUMBER = current_app.config["NUMBER_OF_POKEMON"]
    rand_list = [random.randint(1, 1000) for _ in range(NUMBER)]

    pokemons = []
    for number in rand_list:
        url = f"https://pokeapi.co/api/v2/pokemon/{number}"
        data = get_pokemon(url)
        pokemons.append(data)
    return pokemons

@sync_bp.route('/')
def home():
    start = time.perf_counter()
    pokemons = get_pokemons()
    end = time.perf_counter()

    return render_template(
        'sync.html',
        title="Pokemon Synchronous Version",
        heading="Pokemon Synchronous Version",
        pokemons=pokemons,
        start_time=start,
        end_time=end
    )