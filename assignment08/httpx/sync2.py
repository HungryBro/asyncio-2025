import requests      # นำเข้าไลบรารีสำหรับส่ง HTTP requests แบบ synchronous
import time          # นำเข้า time เพื่อจับเวลา

# สร้างลิสต์ urls ที่มี 5 ตัว (ลิงก์เดียวกันซ้ำ 5 ครั้ง)
# ซึ่งแต่ละลิงก์จะหน่วงเวลา 2 วินาทีก่อนตอบกลับ
urls = ['https://httpbin.org/delay/2',] * 5

# จับเวลาการทำงานก่อนเริ่ม
start = time.time()

# วนลูปทีละลิงก์ (แบบ synchronous = ทีละตัว)
for url in urls:
    response = requests.get(url)  # รอ 2 วินาทีต่อ request
    print(f'Status Code: {response.status_code}')  # แสดง status code เช่น 200

# คำนวณเวลาใช้ทั้งหมดหลังจากโหลดครบทั้ง 5 ลิงก์
print(f'Total time : {time.time() - start} seconds')
