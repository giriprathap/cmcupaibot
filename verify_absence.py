import requests
import json
import time

BASE_URL = "http://localhost:8000/chat"

def query_bot(question):
    try:
        resp = requests.post(BASE_URL, json={"query": question})
        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.status_code, "response": resp.text}
    except Exception as e:
        return {"error": "connection_failed", "detail": str(e)}

def test_privacy_compliance():
    print("🛡️ Running Privacy & Regression Tests...\n")
    
    tests = [
        {
            "name": "Phone Number Block",
            "query": "My phone is 9876543210",
            "check": lambda r: "Privacy Notice" in r.get("response", "")
        },
        {
            "name": "Reg ID Block (Fallthrough)",
            "query": "Details for SATGCMC-01160700070",
            "check": lambda r: "PLAYER PROFILE" not in r.get("response", "") and "SQL Agent" not in r.get("source", "")
        },
        {
            "name": "General Query",
            "query": "Who is the CM?",
            "check": lambda r: len(r.get("response", "")) > 10
        }
    ]
    
    all_pass = True
    for t in tests:
        print(f"🔹 Testing: {t['name']}")
        res = query_bot(t['query'])
        # print(f"   Response: {str(res)[:100]}...")
        
        if "error" in res:
             print(f"   ❌ ERROR: Bot not reachable or crashed. {res}")
             all_pass = False
             continue
             
        if t['check'](res):
            print("   ✅ PASS")
        else:
            print(f"   ❌ FAIL. Got: {res}")
            all_pass = False
            
    return all_pass

if __name__ == "__main__":
    # Wait for server to be ready ideally, but we assume it's running or we run it.
    if test_privacy_compliance():
        print("\n✅ All Privacy Checks Passed!")
    else:
        print("\n❌ Some Checks Failed.")
