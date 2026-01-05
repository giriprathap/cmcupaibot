import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_google_model(model_name):
    print(f"\n--- Testing Google Model: {model_name} ---")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response Body:\n" + json.dumps(response.json(), indent=2))
        except:
            print("Response Body:\n" + response.text)
            
        if response.status_code == 200:
            print("✅ Model FOUND and working.")
        else:
            print("❌ Model Request Failed.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_openai_model(model_name):
    print(f"\n--- Testing OpenAI Model: {model_name} ---")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found.")
        return

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.5
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response Body:\n" + json.dumps(response.json(), indent=2))
        except:
            print("Response Body:\n" + response.text)

        if response.status_code == 200:
            print("✅ Model FOUND and working.")
        else:
            print("❌ Model Request Failed.")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    print("🔍 VERIFYING REQUESTED MODELS (Direct API Call, No LiteLLM)")
    test_google_model("gemini-2.5-flash")
    test_openai_model("gpt-5.2-pro")
