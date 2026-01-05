import sys
import os
import re
from fastapi.testclient import TestClient

# Ensure we can import from the root
sys.path.append(os.getcwd())

from api.main import app

client = TestClient(app)

def test_routes():
    print("🧪 STARTING ROUTING TEST")
    
    # 1. Test Player Lookup (with valid phone number from CSV)
    # Using '7416613302' from player_details.csv
    phone = "7416613302"
    print(f"\n1️⃣  Testing Lookup Route (Phone: {phone})...")
    
    try:
        response = client.post("/ask", json={"question": f"Status for {phone}"})
        if response.status_code == 200:
            ans = response.json().get("answer", "")
            if "CM CUP PLAYER STATUS" in ans:
                print("✅ PASSED: Correctly routed to Lookup and found player!")
                print(f"Output snippet: {ans[:100]}...")
            else:
                print(f"⚠️  ROUTE WARNING: Got 200 but unexpected content: {ans[:100]}")
        else:
            print(f"❌ FAILED: Status Code {response.status_code}")
    except Exception as e:
        print(f"❌ CRITICAL FAIL: {e}")

    # 2. Test RAG (New Data Check)
    print("\n2️⃣  Testing RAG Route (Fixture Question)...")
    try:
        # Asking about data from tb_fixtures.csv
        q = "Tell me about the match schedule for Fixture ID 1"
        response = client.post("/ask", json={"question": q})
        if response.status_code == 200:
            ans = response.json().get("answer", "")
            print(f"✅ PASSED: RAG Answered.")
            print(f"ANSWER: {ans[:200]}...")
        else:
            print(f"ℹ️  RAG Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  RAG FAIL: {e}")

if __name__ == "__main__":
    test_routes()
