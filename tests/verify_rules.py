
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8007"

def test_rules_flow():
    session_id = f"test_rules_{int(time.time())}"
    print(f"Testing Rules Flow with Session ID: {session_id}")
    
    # 1. Main Menu
    send_query("hi", session_id)
    
    # 2. Go to Sports & Matches
    send_query("2", session_id) # Sports matches
    
    # 3. Go to Disciplines
    send_query("1", session_id) # Disciplines -> Returns Level Prompt
    
    # 4. Select Level 1 (Cluster)
    send_query("1", session_id) # Select Cluster Level -> Returns Sports List
    
    # 5. Select Sport "Kho-Kho"
    resp = send_query("Kho-Kho", session_id)
    
    # 5. Select Rules (Option 3)
    resp = send_query("3", session_id)
    
    # Checks
    print("-" * 50)
    print("BOT RESPONSE:")
    print(resp)
    print("-" * 50)
    
    assert "Rules for Kho-Kho" in resp, "Header missing"
    assert "rulebook is currently being updated" not in resp, "Still showing placeholder!"
    # Basic check for content
    assert len(resp) > 100, "Response too short, likely failed."
    
    print("✅ Rules Flow Verified Successfully!")

def send_query(text, session_id):
    url = f"{BASE_URL}/chat"
    payload = {"query": text, "session_id": session_id}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception as e:
        print(f"Request Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_rules_flow()
