
import requests
import json
import sys

BASE_URL = "http://localhost:8000/whatsappchat"

def test_query(query, description):
    print(f"\n--- Testing: {description} ('{query}') ---")
    payload = {
        "user_message": query,
        "phone_number": "9999999999"  # Dummy ID
    }
    
    try:
        response = requests.post(BASE_URL, json=payload)
        if response.status_code != 200:
            print(f"FAILED: Status Code {response.status_code}")
            print(response.text)
            return
            
        data = response.json()
        print("Response Keys:", list(data.keys()))
        
        # Verify Structure
        if "text" not in data:
            print("FAILED: Missing 'text' key")
        else:
            print(f"Text Present: {len(data['text'])} chars")
            
        if "menus" not in data:
            print("FAILED: Missing 'menus' key")
        elif not isinstance(data["menus"], list):
            print("FAILED: 'menus' is not a list")
        else:
            print(f"Menus Count: {len(data['menus'])}")
            if data["menus"]:
                print("First Menu Item:", data["menus"][0])
                
        # print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Test 1: Main Menu
    test_query("menu", "Main Menu")
    
    # Test 2: Simple Query (No Menu)
    test_query("Where is the venue?", "General Query (No Menu)")
    
    # Test 3: Submenu (Mocking state requires session persistence, but we can verify response format)
    # Since session is phone_number based, sending '1' after 'menu' should work if server kept state.
    test_query("1", "Submenu Selection (Registration)")
