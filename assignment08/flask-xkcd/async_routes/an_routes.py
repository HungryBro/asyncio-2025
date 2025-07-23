import time
import random
import asyncio
import httpx
from flask import Blueprint, render_template, current_app

# Create blueprint for async route
async_bp = Blueprint("async", __name__)

# async function to fetch 1 comic
async def fetch_xkcd(url, client):
    response = await client.get(url)
    print(f"{time.ctime()} - get {url}")
    return response.json()

# async function to fetch many comics
async def fetch_xkcds():
    NUMBER_OF_XKCD = current_app.config["NUMBER_OF_XKCD"]
    comic_ids = [random.randint(0, 300) for _ in range(NUMBER_OF_XKCD)]

    async with httpx.AsyncClient() as client:
        tasks = [fetch_xkcd(f'https://xkcd.com/{cid}/info.0.json', client) for cid in comic_ids]
        results = await asyncio.gather(*tasks)
    return results

# async route
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    comics = await fetch_xkcds()
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Get {len(comics)} xkcd. Time taken: {end_time-start_time} seconds")
    return render_template("async.html",
                           title="XKCD Asynchronous Flask",
                           heading="XKCD Asynchronous Version",
                           xkcds=comics,
                           start_time=start_time,
                           end_time=end_time)
