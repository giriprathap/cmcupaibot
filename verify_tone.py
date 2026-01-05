import requests
import json

def test_query(query, description):
    print(f"\n🔎 Testing [{description}]: '{query}'")
    try:
        response = requests.post(
            "http://localhost:8001/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            res_json = response.json()
            print("Response:\n" + ("-"*40))
            print(res_json.get("response"))
            print("-" * 40)
        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    # 1. Structure Check: Should list sports in bullets
    test_query("games", "Structure: Sports List")
    
    # 2. Tone Check: Should be formal
    test_query("eligibility", "Tone: Eligibility")

    # 3. Context Quality Check
    test_query("Who organizes this event?", "Checking for usage of Context Quality debug info")

    # 4. Confidence Check
    test_query("Can I download the schedule?", "Checking for unconfident phrases")
