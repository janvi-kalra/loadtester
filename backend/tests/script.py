import requests

url = "http://127.0.0.1:8000/loadtest"
payload = {
    "url": "http://example.com",
    "qps": 10,
    "duration": 5
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Test results:")
    print(response.json())
else:
    print(f"Failed to run load test: {response.status_code}")
