import asyncio
import httpx
import time

student_id = "6610301004"

# ปรับเพิ่ม argument start_time เพื่อให้กำหนดเวลาเริ่มพร้อมกันได้
async def fire_rocket(name: str, t0: float, start_time: float):
    url = f"http://127.0.0.1:8088/fire/{student_id}"  # เปลี่ยนเป็น localhost uvicorn บนเครื่องตัวเอง

    # ใช้ start_time ที่ส่งเข้ามาแทนการจับเวลาใหม่ (ทุก rocket เริ่มพร้อมกัน)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        time_to_target = float(data.get("time_to_target", 0))

    end_time = time.perf_counter() - t0  # เวลาที่ rocket ถึงเป้าหมาย

    return {
        "name": name,
        "start_time": start_time,
        "time_to_target": time_to_target,
        "end_time": end_time,
    }

async def main():
    t0 = time.perf_counter()
    print("Rocket prepare to launch ...")

    # TODO: จับเวลาเริ่มครั้งเดียว แล้วส่งให้ทุก rocket
    common_start = time.perf_counter() - t0

    # TODO: ยิง rocket 1–3 ตามลำดับ
    tasks = [
        asyncio.create_task(fire_rocket(f"Rocket-{i+1}", t0, common_start))
        for i in range(3)
    ]

    # TODO: รอให้ทุก task เสร็จและเก็บผลลัพธ์ตามลำดับ task
    results = await asyncio.gather(*tasks)

    # TODO: แสดงผล start_time, time_to_target, end_time ของแต่ละ rocket ตามลำดับ task
    print("Rockets fired:")
    for r in results:
        print(
            f"{r['name']} | start_time: {r['start_time']:.2f} sec "
            f"| time_to_target: {r['time_to_target']:.2f} sec "
            f"| end_time: {r['end_time']:.2f} sec"
        )

    # TODO: แสดงเวลารวมทั้งหมดตั้งแต่ยิงลูกแรกจนลูกสุดท้ายถึงจุดหมาย
    t_total = max(r["end_time"] for r in results)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

if __name__ == "__main__":
    asyncio.run(main())
