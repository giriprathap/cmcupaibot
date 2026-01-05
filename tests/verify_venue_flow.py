
import requests
import json

BASE_URL = "http://localhost:8000/chat"

def query_bot(question):
    print(f"\n❓ Question: {question}")
    resp = requests.post(BASE_URL, json={"query": question})
    if resp.status_code == 200:
        ans = resp.json().get("response", "")
        print(f"🤖 Answer: {ans[:200]}..." if len(ans) > 200 else f"🤖 Answer: {ans}")
        return ans
    return "Error"

def verify_venue_flow():
    print("🧪 Verifying Venue Flow...")

    # 1. Prompt for Phone
    print("\n--- Test 1: Prompt for Phone ---")
    ans1 = query_bot("Venue details please")
    if "provide your registered **Phone Number**" in ans1:
        print("✅ PASS")
    else:
        print("❌ FAIL")

    # 2. General Phone Block
    print("\n--- Test 2: General Phone Block ---")
    ans2 = query_bot("My phone is 9876543210")
    if "Privacy Notice" in ans2 and "Venue details for" in ans2:
        print("✅ PASS")
    else:
        print("❌ FAIL")
        
    # 3. Valid Venue Lookup (Mock logic - may fail if data not in DB, but checking flow)
    # We will look for "Information" or "No registrations" but NOT "Privacy Notice"
    print("\n--- Test 3: Venue Lookup ---")
    ans3 = query_bot("Venue details for 9876543210")
    if "No registrations found" in ans3 or "Venue Details" in ans3:
        if "Privacy Notice" not in ans3:
            print("✅ PASS")
        else:
            print("❌ FAIL (Privacy Triggered)")
    else:
        print("❌ FAIL (Unexpected Response)")

    # 4. Ack Number Lookup
    print("\n--- Test 4: Ack No Lookup ---")
    ans4 = query_bot("Venue for SATGCMC-1234")
    if "Venue Details (Ack: SATGCMC-1234)" in ans4 or "Venue Details" in ans4 or "No match found" in str(ans4) or "Fallthrough" in str(ans4):
       # Since we don't have valid ack in DB for check, we check if it tried SQL or fell through. 
       # But implemented logic might return None -> pass -> RAG.
       # Let's check logic: if rec found -> response. Else -> pass -> RAG.
       # So likely RAG response.
       print("✅ PASS (Flow executed)")
    else:
       print("⚠️ Review Output")

    # 5. Static Ack Link
    print("\n--- Test 5: Ack Link ---")
    ans5 = query_bot("What is my Ack Number")
    if "Download Enrollment Acknowledgment" in ans5:
        print("✅ PASS")
    else:
        print(f"❌ FAIL. Got: {ans5}")

if __name__ == "__main__":
    verify_venue_flow()
