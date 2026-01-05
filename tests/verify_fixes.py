import requests
import json
import time

def test_query(query, name):
    print(f"\n🧪 Testing [{name}] Query: '{query}'")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            res_json = response.json()
            res_text = res_json.get("response", "")
            source = res_json.get("source", "")
            
            print(f"🔹 Source: {source}")
            print(f"🔹 Response Length: {len(res_text)}")
            print("Response Preview:\n" + ("-"*40))
            print(res_text[:300] + "..." if len(res_text) > 300 else res_text)
            print("-" * 40)
            
            # Check for JSON leak
            if list(set(res_text.strip())) == ['{'] or '{"response":' in res_text[:20]:
                print("❌ FAIL: JSON Leak Detected in output!")
            else:
                print("✅ PASS: Output looks like plain text.")

            # Check for SATG vs SATS
            if "SATG" in res_text:
                print("✅ PASS: Found 'SATG'")
            elif "SATS" in res_text:
                print("❌ FAIL: Found 'SATS' (Should be SATG)")
            
            # Check for Fallback "Not available"
            if "not currently available in my database" in res_text:
                print("⚠️ CAUTION: Found old fallback phrase (might be expected if regex didn't catch all variants)")
            elif "I couldn't find specific details" in res_text:
                 print("✅ PASS: Found new fallback phrase")

        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    # 1. Transport (Likely fallback or empty context)
    test_query("Is transport provided?", "Transport Check")
    time.sleep(1)

    # 2. Organizer (Check SATG vs SATS)
    test_query("Who is organizing this event?", "Organizer Check")
    time.sleep(1)

    # 3. Matches Near Me (History of JSON Leak)
    test_query("Are matches near me?", "JSON Leak Check")
