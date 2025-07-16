import asyncio
import httpx

async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return url, response.status_code
    
async def main():
    urls = [
        'https://example.com',
        'https://httpbin.org/get',
        'https://api.github.com',
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, status in results:
        print(f'URL: {url} → Status Code: {status}')

asyncio.run(main())