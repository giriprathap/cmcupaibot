import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/chat"

def test_lookup(val, desc):
    print(f"\n🧪 Testing {desc}: {val}")
    try:
        start = time.time()
        res = requests.post(BASE_URL, json={"query": val})
        lat = time.time() - start
        
        if res.status_code == 200:
            data = res.json()
            src = data.get("source")
            txt = data.get("response", "")
            
            print(f"   ✅ Success ({lat:.2f}s) | Source: {src}")
            if "Cluster Details" in txt:
                print("      - Cluster Info Found ✅")
            else:
                print("      - Cluster Info MISSING ❌")
                
            if "Game & Schedule" in txt:
                 print("      - Schedule Found ✅")
        else:
            print(f"   ❌ Failed: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"   ⚠️ Error: {e}")

if __name__ == "__main__":
    # Wait for server to boot
    time.sleep(2)
    
    # Test valid phone (picked from logs/schema analysis)
    # Assume 1234567890 is a valid mock or pick one from player_details if known. 
    # From debug_schema, we saw player_details exists. I'll rely on the user having valid data or use a generic one.
    # Actually, previous stress test used 1234567890 and got "No Record".
    # I should try to pick a REAL phone number from the CSV if I can?
    # I'll use a broad test query that implies lookup.
    
    test_lookup("9959648666", "Phone Number (Real)")
    test_lookup("SATGCMC25-001", "Reg ID (Mock)")
