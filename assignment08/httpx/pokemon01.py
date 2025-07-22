# นำเข้าไลบรารี requests สำหรับส่ง HTTP requests แบบ synchronous
import requests

# กำหนด URL ของ API ที่จะเรียกข้อมูลโปเกมอนชื่อ "pikachu"
url = 'https://pokeapi.co/api/v2/pokemon/pikachu'

# ส่ง HTTP GET request ไปยัง URL แล้วเก็บ response ไว้ในตัวแปร response
response = requests.get(url)

# แปลงข้อมูล JSON จาก response เป็น Python dictionary แล้วเก็บไว้ในตัวแปร data
data = response.json()

# แสดงชื่อของโปเกมอน จาก key 'name'
print("Name:", data['name'])

# แสดง ID ของโปเกมอน จาก key 'id'
print("ID:", data['id'])

# แสดงความสูงของโปเกมอน (หน่วยเป็น decimetres) จาก key 'height'
print("Height:", data['height'])

# แสดงน้ำหนักของโปเกมอน (หน่วยเป็น hectograms) จาก key 'weight'
print("Weight:", data['weight'])

# แสดงประเภทของโปเกมอน เช่น ['electric']
# โดยวนลูปใน data['types'] แล้วดึงชื่อของแต่ละ type
print("Types:", [t['type']['name'] for t in data['types']])
