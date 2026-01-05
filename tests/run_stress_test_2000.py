
import requests
import json
import time
import pandas as pd
from datetime import datetime
import os
from tqdm import tqdm

# Config
API_URL = "http://localhost:8000/chat"
QUESTIONS_FILE = r"tests/extracted_questions.txt"
OUTPUT_FILE = r"tests/stress_test_results_2000.csv"
RATE_LIMIT_DELAY = 1.6  # Seconds between requests (Conservative for free tier)
MAX_RETRIES = 2

def run_test():
    print("🚀 Starting Stress Test Runner (2000 Questions)")
    
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
        if i > 0 and i % 50 == 0:
            # Save intermediate results
            pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
            
        success = False
        response_text = ""
        source = ""
        latency = 0
        error_msg = ""
        
        start_time = time.time()
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = requests.post(
                    API_URL, 
                    json={"query": q}, 
                    timeout=30 # Long timeout for RAG
                )
                latency = round(time.time() - start_time, 2)
                
                if resp.status_code == 200:
                    data = resp.json()
                    success = True
                    response_text = str(data.get("response", ""))
                    source = str(data.get("source", "unknown"))
                    break # Success
                else:
                    error_msg = f"HTTP {resp.status_code}: {resp.text}"
                    time.sleep(2) # Backoff
                    
            except Exception as e:
                error_msg = str(e)
                time.sleep(2) # Backoff
        
        # Log Result
        results.append({
            "id": i + 1,
            "query": q,
            "success": success,
            "response_text": response_text[:500], # Truncate for CSV
            "source": source,
            "latency_sec": latency,
            "error": error_msg
        })
        
        # Rate Limit Sleep
        time.sleep(RATE_LIMIT_DELAY)

    # Final Save
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Stress test complete. Results saved to {OUTPUT_FILE}")
    
    # Quick Summary
    passed = df[df['success'] == True]
    print(f"Total: {len(df)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(df) - len(passed)}")
    print(f"Avg Latency: {df['latency_sec'].mean():.2f}s")
    print(f"Sources: {df['source'].value_counts().to_dict()}")

if __name__ == "__main__":
    run_test()
