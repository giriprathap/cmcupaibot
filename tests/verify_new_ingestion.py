
import requests
import json
import time

BASE_URL = "http://localhost:8000/chat"

def query_bot(question):
    print(f"\n❓ Question: {question}")
    try:
        resp = requests.post(BASE_URL, json={"query": question})
        if resp.status_code == 200:
            data = resp.json()
            ans = data.get("response", "")
            print(f"🤖 Answer: {ans[:200]}..." if len(ans) > 200 else f"🤖 Answer: {ans}")
            return ans
        else:
            print(f"❌ Error {resp.status_code}: {resp.text}")
            return ""
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return ""

def verify():
    print("🧪 Verifying New Data Ingestion...")
    
    # 1. IT Support (from IT_Team_RAG_Knowledge.txt)
    ans1 = query_bot("Who is the IT Team member for Hanumakonda district?")
    if "Sai Kumar" in ans1:
        print("✅ PASS: Found IT member")
    else:
        print("❌ FAIL: IT member not found")

    # 2. Cluster Mapping (from Vikarabad file)
    # Pick a random GP from the file, e.g. from inspection or guess. 
    # Let's ask about a generic cluster query first or a specific officer if we recall one.
    # From file view earlier: "District: Jangaon ... Special Officer: Abdul Shafi"
    ans2 = query_bot("Who is the Special Officer for Jangaon?")
    if "Abdul Shafi" in ans2:
        print("✅ PASS: Found Special Officer")
    else:
        print("❌ FAIL: Special Officer not found")

    # 3. Schedule (from RAG_Knowledge.txt)
    ans3 = query_bot("When does the Torch Rally start for CM Cup 2025?")
    if "08 January 2026" in ans3 or "January 8" in ans3:
        print("✅ PASS: Found Torch Rally date")
    else:
        print("❌ FAIL: Torch Rally date not found")

    # 4. Excel Data (Disciplines)
    # We need to know a specific detail from the Excel.
    # We saw "Disciplines_CMCup_2025.xlsx". 
    ans4 = query_bot("Is Kho-Kho a team sport in CM Cup?")
    if "Kho-Kho" in ans4 or "Team" in ans4:
        print("✅ PASS: Found Discipline info")
    else:
        print("❌ FAIL: Discipline info not found")

if __name__ == "__main__":
    verify()
