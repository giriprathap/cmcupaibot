
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from api.main import chat_endpoint, ChatRequest

async def run_tests():
    print("🧪 Starting Privacy Verification...")

    # Test 1: Phone Number (Should Trigger Warning)
    print("\n[Test 1] Phone Number Query")
    req1 = ChatRequest(query="Check status for 9876543210")
    try:
        res1 = await chat_endpoint(req1)
        print("Response:", res1)
        if "Privacy Notice" in res1.get("response", "") and "do not share personal phone numbers" in res1.get("response", ""):
            print("✅ SUCCESS: Privacy Warning Triggered")
        else:
            print("❌ FAILURE: Privacy Warning NOT Triggered")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # Test 2: Reg ID (Should Fallthrough / Not Show Card)
    print("\n[Test 2] Reg ID Query")
    req2 = ChatRequest(query="Details for SATGCMC-01160700070")
    try:
        res2 = await chat_endpoint(req2)
        print("Response:", res2)
        resp_text = res2.get("response", "")
        # It should NOT be a player card
        if "PLAYER PROFILE" in resp_text or "**Info**" in resp_text:
             print("❌ FAILURE: Player Card still shown!")
        else:
             print("✅ SUCCESS: Player Card NOT shown (Fallthrough behavior)")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # Test 3: General Query (Should pass)
    print("\n[Test 3] General Query")
    req3 = ChatRequest(query="Who is the CM?")
    try:
        res3 = await chat_endpoint(req3)
        # We just want a response, don't care about exact content for this specific test, as long as it doesn't crash
        if res3 and res3.get("response"):
             print(f"✅ SUCCESS: General query returned response: {res3.get('response')[:50]}...")
        else:
             print("❌ FAILURE: General query failed")
    except Exception as e:
         print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_tests())
