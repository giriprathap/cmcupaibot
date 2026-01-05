
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8015"

def test_schedules_flow():
    session_id = f"test_sched_{int(time.time())}"
    print(f"Testing Schedules Flow with Session ID: {session_id}")
    
    # 1. Main Menu
    send_query("hi", session_id)
    
    # 2. Go to Sports & Matches
    send_query("2", session_id) 
    
    # 3. Select Schedules (Option 2) - SHOULD now go to submenu
    resp = send_query("2", session_id)
    assert "Tournament Schedules" in resp, "Submenu Header Missing"
    assert "Games Schedules" in resp, "Submenu Options Missing"
    
    # 4. Test Option 1: Tournament Schedules
    resp = send_query("1", session_id)
    assert "Mandal Level" in resp, "Tournament Info Missing"
    assert "Jan 15" in resp, "Dates Missing"
    
    print("✅ Tournament Schedule Verified")
    
    # 5. Back to Submenu
    send_query("Back", session_id)
    
    # 6. Test Option 2: Games Schedules
    # "2" from Sports Menu -> Enters Schedule Submenu
    resp = send_query("2", session_id)
    assert "Tournament Schedules" in resp, "Not in Submenu?"
    
    # NOW Select Option 2 INSIDE Submenu
    resp = send_query("2", session_id)
    assert "Games Schedules" in resp, "Games Header Missing"
    assert "Which sport" in resp, "Sport Prompt Missing"
    
    # 7. Check valid sport (Kabaddi)
    resp = send_query("Kabaddi", session_id)
    print(f"DEBUG: Response for Kabaddi: {resp}")
    assert "viewschedulegames" in resp, "Schedule Link Missing"
    assert "Kabaddi" in resp, "Sport Name Missing"
    # The current DB data might return "No specific schedule found" or actual schedule 
    # depending on data, but we just check we got a response.
    # We can check for "Schedule" or "Date" or "Time" or "No specific schedule"
    
    # Just ensure we aren't in the menu loop or error
    print("✅ Games Schedule Verified")
    
    print("✅ All Schedule Flows Verified Successfully!")

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
    test_schedules_flow()
