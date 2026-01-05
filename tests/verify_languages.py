import requests
import json
import time

def test_multilingual(query, name, script_hint):
    print(f"\n🌍 Testing [{name}] Query: '{query}'")
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            res_text = response.json().get("response", "")
            print("Response:\n" + ("-"*40))
            print(res_text[:200] + "..." if len(res_text) > 200 else res_text)
            print("-" * 40)
            
            # Simple heuristic check
            print(f"👉 Verify this looks like: {script_hint}")
        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    # 1. Hindi (Devanagari)
    test_multilingual("आयोजक कौन है?", "Hindi", "Devanagari")
    time.sleep(1)

    # 2. Telugu
    test_multilingual("ఈ ఈవెంట్‌ను ఎవరు నిర్వహిస్తున్నారు?", "Telugu", "Telugu Script")
    time.sleep(1)

    # 3. Hinglish
    test_multilingual("Event ka organizer kaun hai?", "Hinglish", "Roman Hindi (Hinglish)")
    time.sleep(1)

    # 4. English
    test_multilingual("Who is the organizer?", "English", "English")
