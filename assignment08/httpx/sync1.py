import requests

response = requests.get('https://httpbin.org/delay/3')
print(f'Status Code: {response.status_code}')