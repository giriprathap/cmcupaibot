
import requests
import json
import time
import pandas as pd
from datetime import datetime
import os
from tqdm import tqdm

# Config
API_URL = "http://localhost:8000/chat"
QUESTIONS_FILE = r"tests/cmcup_questions.txt"
OUTPUT_FILE = r"tests/stress_test_results_cmcup.csv"
RATE_LIMIT_DELAY = 1.0  # Slightly faster for 50 questions
MAX_RETRIES = 2

def run_test():
    print("🚀 Starting CM Cup Stress Test Runner")
    
    # Load Questions
    if not os.path.exists(QUESTIONS_FILE):
        print(f"❌ Questions file not found: {QUESTIONS_FILE}")
        return
        
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(questions)} questions.")
    
    results = []
    
    # Check if API is alive
    try:
        requests.get("http://localhost:8000/health", timeout=5)
        print("✅ API is responding.")
    except Exception:
        print("❌ API is NOT responding. Please start uvicorn!")
        return

    # Run Loop
    for i, q in enumerate(tqdm(questions, desc="Testing")):
        if i > 0 and i % 10 == 0:
            pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
            
        success = False
        response_text = ""
        source = ""
        latency = 0
        error_msg = ""
        model_used = ""
        
        start_time = time.time()
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = requests.post(
                    API_URL, 
                    json={"query": q}, 
                    timeout=45 
                )
                latency = round(time.time() - start_time, 2)
                
                if resp.status_code == 200:
                    data = resp.json()
                    success = True
                    response_text = str(data.get("response", ""))
                    source = str(data.get("source", "unknown"))
                    # Try to extract model if embedded in response text (rare) or if we add it to API response
                    # Currently API only returns response/source/intent usually? 
                    # Actually, our ask_llm returns "model_used" but main.py might filter it.
                    # Let's check main.py output later.
                    break 
                else:
                    error_msg = f"HTTP {resp.status_code}: {resp.text}"
                    time.sleep(2) 
                    
            except Exception as e:
                error_msg = str(e)
                time.sleep(2)
        
        results.append({
            "id": i + 1,
            "query": q,
            "success": success,
            "response_text": response_text[:1000],
            "source": source,
            "latency_sec": latency,
            "error": error_msg
        })
        
        time.sleep(RATE_LIMIT_DELAY)

    # Final Save
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Stress test complete. Results saved to {OUTPUT_FILE}")
    
    # Quick Summary
    passed = df[df['success'] == True]
    print(f"Total: {len(df)}")
    print(f"Passed: {len(passed)}")
    print(f"Avg Latency: {df['latency_sec'].mean():.2f}s")
    print(f"Sources: {df['source'].value_counts().to_dict()}")

if __name__ == "__main__":
    run_test()
