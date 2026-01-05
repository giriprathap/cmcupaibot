import requests
import json

url = "http://127.0.0.1:8000/whatsappchat"
headers = {"Content-Type": "application/json"}
payload = {
    "user_message": "Games",
    "first_name": "Giriprathap Raju",
    "phone_number": "919703662169"
}

try:
    print(f"Sending POST to {url} with payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    if response.status_code == 200:
        print("\n✅ SUCCESS: Endpoint returned 200 OK")
    else:
        print(f"\n❌ FAILURE: Endpoint returned {response.status_code}")

except Exception as e:
    print(f"❌ ERROR: Could not connect to API. Is it running? {e}")
