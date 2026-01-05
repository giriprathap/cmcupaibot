
import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def test_menu_flow():
    # 1. Start Session
    session_id = "test_verification_sess"
    print(f"Testing Menu Flow with Session ID: {session_id}")
    
    # 2. Main Menu
    resp = send_query("hi", session_id)
    assert "Registration & Eligibility" in resp, "Main Menu missing Option 1"
    assert "Sports & Matches" in resp, "Main Menu missing Option 2"
    assert "Help & Language" in resp, "Main Menu missing Option 5"
    print("✅ Main Menu Verified")
    
    # 3. Registration (Option 1)
    resp = send_query("1", session_id)
    assert "How to Register" in resp, "Reg Menu missing Option 1"
    assert "Eligibility Rules" in resp, "Reg Menu missing Option 2"
    print("✅ Registration Menu Verified")
    
    # 4. Eligibility Check (Option 2) -> Sport Age Input
    resp = send_query("2", session_id)
    assert "Eligibility Check" in resp or "Sport" in resp, "Eligibility Check prompt missing"
    
    # 5. Enter Sport "Kabaddi"
    resp = send_query("Kabaddi", session_id)
    assert "Age Criteria for Kabaddi" in resp, "Age Criteria lookup failed"
    print("✅ Eligibility Flow Verified")
    
    # 6. Back to Main
    resp = send_query("Back", session_id) # Back to Reg
    resp = send_query("Back", session_id) # Back to Main
    assert "Registration & Eligibility" in resp, "Failed to return to Main Menu"
    
    # 7. Sports & Matches (Option 2)
    resp = send_query("2", session_id)
    assert "Sports Disciplines" in resp, "Sports Menu missing Option 1"
    
    # 8. Schedules (Option 2) -> Sport Schedule Input
    resp = send_query("2", session_id) # Schedules
    assert "Which sport" in resp, "Schedule prompt missing"
    
    # 9. Enter Sport "Athletics"
    resp = send_query("Athletics", session_id)
    assert "Schedule" in resp or "schedule" in resp, "Schedule lookup failed"
    print("✅ Schedule Flow Verified")

    print("\n🎉 ALL CHECKS PASSED!")

def send_query(text, session_id):
    url = f"{BASE_URL}/chat"
    payload = {"query": text, "session_id": session_id}
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        response = data.get("response", "")
        # print(f"User: {text} -> Bot: {response[:50]}...")
        return response
    except Exception as e:
        print(f"Request Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_menu_flow()
