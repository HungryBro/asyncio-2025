import requests
import time

urls = ['https://httpbin.org/delay/2',] * 5

start = time.time()
for url in urls:
    response = requests.get(url)
    print(f'Status Code: {response.status_code}')
print(f'Total time : {time.time() - start} seconds')