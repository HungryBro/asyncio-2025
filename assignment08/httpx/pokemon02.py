# นำเข้า requests สำหรับส่ง HTTP request
import requests

# นำเข้า time เพื่อจับเวลา
import time

# รายชื่อโปเกมอนที่ต้องการดึงข้อมูล
pokemon_name = ["pikachu", "bulbasaur", "charmander", "squirtle", "snorlax"]

# บันทึกเวลาก่อนเริ่มลูป
start = time.time()

# วนลูปผ่านชื่อโปเกมอนแต่ละตัว
for name in pokemon_name:
    # สร้าง URL สำหรับเรียกข้อมูลแต่ละตัวจาก PokeAPI
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    
    # ส่ง HTTP GET request
    response = requests.get(url)
    
    # แปลงข้อมูล JSON เป็น dict
    data = response.json()
    
    # แสดงชื่อ, ID และประเภทของโปเกมอน
    print(f"{data['name'].title()} → ID: {data['id']}, Types: {[t['type']['name'] for t in data['types']]}")

# บันทึกเวลาหลังจบลูป
end = time.time()

# แสดงเวลาที่ใช้ทั้งหมด (แก้รูปแบบการใช้ round ให้ถูกต้อง)
print(f'Total time : {round(end - start, 2)} seconds')
