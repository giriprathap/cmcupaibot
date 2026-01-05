
import requests
import json

url = "http://localhost:8000/chat"
payload = {"query": "disciplines cluster level "}
headers = {"Content-Type": "application/json"}

try:
    print(f"Sending POST to {url} with payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
