import httpx, json
url = 'http://127.0.0.1:8009/auth/login'
payload = {"email": "admin@library.com", "password": "admin123"}
response = httpx.post(url, json=payload)
print('Status:', response.status_code)
print('Response:', response.json())
