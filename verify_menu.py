import requests
import json
import time

url = "http://127.0.0.1:8000/chat"

def send(query, session_id="test_fuzzy_v2"):
    payload = {"query": query, "session_id": session_id}
    print(f"\nUser: {query}")
    try:
        resp = requests.post(url, json=payload).json()
        print(f"Bot: {resp.get('response')[:300]}...") 
        return resp
    except Exception as e:
        print(f"Error: {e}")
        return {}

# 1. Start Session
send("menu")

# 2. Go to Officers Menu
send("5") 

# 3. Test Partial Match ("Akine")
send("Akine")

# 4. Test User's Reported Typo ("Ankinapally")
send("Ankinapally")

# 5. Test Another Typo ("dampeta")
send("dampeta")

# 6. Back
send("Back")
