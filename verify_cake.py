import requests
import json

def test_query(query):
    print(f"\n🔎 Testing Query: '{query}'")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            res_json = response.json()
            print("Response:", json.dumps(res_json.get("response"), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_query("How to bake a cake?")
