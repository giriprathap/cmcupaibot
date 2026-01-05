import requests
import json

def test_query(query, description):
    print(f"\n🔎 Testing [{description}]: '{query}'")
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
    # Type 1: True Absence
    test_query("What is the capital of Mars?", "True Absence")
    
    # Type 2: Date Mismatch / Partial
    test_query("What is cmcup 2015", "Date Mismatch")

    # Type 3: Ambiguous (Vague)
    test_query("details", "Ambiguous")
    
    # Success Case
    test_query("games", "Success Case (Synonym)")
