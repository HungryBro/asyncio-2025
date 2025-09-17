# file: rocketapp.py

from fastapi import FastAPI, HTTPException
import asyncio
import random

app = FastAPI(title="Asynchronous Rocket Launcher")

# เก็บ task ของจรวด (optional)
rockets = []

async def launch_rocket(student_id: str, time_to_target: float):
    """
    TODO:
    - จำลองเวลาจรวดด้วย random delay 1-2 วินาที
    - print log ว่า rocket launched และ reached destination
    """
    
    print(f"Rocket {student_id} launched! ETA: {time_to_target:.2f} seconds")
    await asyncio.sleep(time_to_target)
    print(f"Rocket {student_id} reached destination after {time_to_target:.2f} seconds")

    pass

@app.get("/fire/{student_id}")
async def fire_rocket(student_id: str):
    """
    TODO:
    - ตรวจสอบ student_id ต้องเป็น 10 หลัก
    - สร้าง background task ยิง rocket
    - รอ random delay 1-2 วินาที ก่อนส่ง response
    - return dict {"message": ..., "time_to_target": ...}
    """

    if len(student_id) != 10 or not student_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid student_id, must be 10 digits")

    # สุ่มเวลาจรวดบิน
    time_to_target = random.uniform(1.0, 2.0)

    # สร้าง background task
    task = asyncio.create_task(launch_rocket(student_id, time_to_target))
    rockets.append(task)

    # ส่ง response กลับทันที (ไม่รอ rocket บินเสร็จ)
    return {
        "message": f"Rocket {student_id} fired!",
        "time_to_target": round(time_to_target, 2)
    }

    pass
