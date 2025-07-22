import requests  # นำเข้าไลบรารี requests สำหรับส่ง HTTP requests แบบ synchronous

# ส่ง GET request ไปยัง https://httpbin.org/delay/3
# ซึ่งเป็น API ที่จำลองการหน่วงเวลา 3 วินาทีก่อนตอบกลับ
response = requests.get('https://httpbin.org/delay/3')

# แสดงผลสถานะการตอบกลับ (เช่น 200 OK)
print(f'Status Code: {response.status_code}')
