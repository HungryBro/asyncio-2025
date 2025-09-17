# Hint:
# แก้โค้ดให้สามารถรัน หลาย task พร้อมกัน ได้ถูกต้อง
# Result:
# Processing data
# Processing data
# Processing data
# Processing data
# Processing data

import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return print ("data")

async def process():
    await asyncio.sleep(2)
    data = await fetch_data()
    print("Processing", data)

tasks = [process() for _ in range(5)]

async def main():
    await asyncio.run(*tasks)