
import requests
import json
import time

API_URL = "http://127.0.0.1:8000/ask"

def test_question(question, lang_label):
    print(f"\n[{lang_label}] Asking: {question}")
    try:
        start = time.time()
        response = requests.post(API_URL, json={"question": question}, timeout=30)
        lat = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            # The API might return the dict directly or wrapped. 
            # If api/main.py returns the chain result directly, it will be {"response":..., "model_used":...}
            # But the previous api likely returned {"answer": ...} or similar.
            # I need to see api/main.py result first.
            # Assuming api/main.py adapts it or just returns the dict.
            ans = data.get("response", data.get("answer", ""))
            model = data.get("model_used", "Unknown")
            print(f"✅ Response ({lat:.2f}s) [Model: {model}]: {ans}\n")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

questions = [
    ("What is the address of the Sports Authority?", "English"),
    ("Sports Authority ka address kya hai?", "Hindi"),
    # ("Who is the CM of Telangana?", "English"),
    # ("Telangana ka CM kaun hai?", "Hindi"),
    # ("Telangana CM evaru?", "Telugu"),
]

if __name__ == "__main__":
    print("🌍 Starting Multilingual Test...")
    for q, l in questions:
        test_question(q, l)
