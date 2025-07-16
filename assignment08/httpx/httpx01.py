import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com')
        print(response.status_code)
        print(response.text[:100])  # Print first 100 characters of the response text

asyncio.run(main())