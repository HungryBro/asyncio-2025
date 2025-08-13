import asyncio 

async def download(file_name, size_mb, delay_sec):
    await asyncio.sleep(delay_sec) 
    speed = size_mb / delay_sec
    print(f"{file_name} downloaded at {speed:.2f} MB/s") 

async def main(): 
    tasks = [ asyncio.create_task(download("File A", 300, 3)), 
             asyncio.create_task(download("File B", 200, 2)), 
             asyncio.create_task(download("File C", 100, 1))]
    await asyncio.gather(*tasks)

asyncio.run(main())