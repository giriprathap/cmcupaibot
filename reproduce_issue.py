
import requests
import json

def test_whatsapp_chat():
    url = "http://localhost:8000/whatsappchat"
    payload = {
        "user_message": "menu",
        "phone_number": "9999999999"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_whatsapp_chat()
