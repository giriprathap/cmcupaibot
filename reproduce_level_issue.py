import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_query(query):
    print(f"\nTesting Query: '{query}'")
    try:
        resp = requests.post(f"{BASE_URL}/chat", json={"query": query})
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response: {data.get('response')}")
            print(f"Source: {data.get('source')}")
        else:
            print(f"Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    # Test cases reported by user
    test_query("Mandal Level Game Dates")
    test_query("Mandal Level Venue Details")
    test_query("mandal venue")
    test_query("GP Level cluster details")
    test_query("Incharge for Allipalli cluster")
    test_query("Football starts from which Level")
    
    # Control case
    test_query("Venue details for 9848012345")
