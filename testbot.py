
import requests
import json
import time

API_URL = "http://localhost:8000/chat"

def main():
    print("🤖 RAG Chatbot CLI Tester")
    print(f"📡 Connecting to: {API_URL}")
    print("EXIT/QUIT to stop.\n")
    
    # Check health
    try:
        requests.get("http://localhost:8000/health", timeout=2)
        print("✅ API is Online!\n")
    except:
        print("❌ API seems offline. Make sure 'uvicorn api.main:app' is running.")
        return

    # Pre-defined test queries for quick verification
    test_queries = [
        "How many players are there in total?",
        "Who is the incharge for Shamirpet cluster?",
        "List 3 sports played in Medchal district",
        "Check mobile 9876543210",
        "How many female Kabaddi players are there?"
    ]
    
    print("💡 Tip: Type 'auto' to run automated test suite.")

    while True:
        try:
            query = input("You: ").strip()
            if not query: continue
            if query.lower() in ["exit", "quit", "q"]:
                break
            
            queue = [query]
            if query.lower() == "auto":
                queue = test_queries
                print(f"🚀 Running {len(queue)} Automated Tests...\n")

            for q in queue:
                if len(queue) > 1: print(f"👉 Query: {q}")
                start = time.time()
                try:
                    response = requests.post(
                        API_URL, 
                        json={"query": q},
                        headers={"Content-Type": "application/json; charset=utf-8"},
                        timeout=60
                    )
                    latency = round(time.time() - start, 2)
                    
                    if response.status_code == 200:
                        data = response.json()
                        ans = data.get("response", "No response text")
                        src = data.get("source", "Unknown")
                        
                        # Handle Encoding for Console
                        try:
                            print(f"\n🤖 Bot ({latency}s) [{src}]:\n{'-'*40}")
                            print(ans)
                            print(f"{'-'*40}\n")
                        except UnicodeEncodeError:
                            print(f"\n🤖 Bot ({latency}s) [{src}]:\n{'-'*40}")
                            print(ans.encode('utf-8', errors='ignore').decode('ascii'))
                            print(f"{'-'*40}\n")
                    else:
                        print(f"\n❌ Error {response.status_code}:\n{response.text}\n")
                        
                except Exception as e:
                     print(f"Error: {e}")
            
            if query.lower() == "auto":
                 print("✅ Automated Tests Complete. Back to manual mode.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
