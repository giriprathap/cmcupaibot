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
            print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_query("What is cmcup 2015")
