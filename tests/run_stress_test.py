import requests
import json
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

INPUT_FILE = "data/dataset_1000.json"
OUTPUT_FILE = "tests/stress_test_report_1000.md"
API_URL = "http://127.0.0.1:8000/ask"

def ask_api(question_data):
    q_id = question_data["id"]
    question = question_data["question"]
    topic = question_data["topic"]
    
    max_retries = 3
    for attempt in range(max_retries):
        start_time = time.time()
        try:
            response = requests.post(API_URL, json={"question": question}, timeout=30)
            end_time = time.time()
            latency = round(end_time - start_time, 2)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                is_fallback = "I don't have that information" in answer
                status = "FALLBACK" if is_fallback else "SUCCESS"
                return {
                    "id": q_id,
                    "topic": topic,
                    "question": question,
                    "answer": answer,
                    "latency": latency,
                    "status": status,
                    "error": None
                }
            elif response.status_code == 429:
                print(f"⚠️ 429 Rate Limit. Sleeping 60s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(60)
                continue
            else:
                return {
                    "id": q_id,
                    "topic": topic,
                    "question": question,
                    "answer": "",
                    "latency": latency,
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "id": q_id,
                "topic": topic,
                "question": question,
                "answer": "",
                "latency": 0,
                "status": "ERROR",
                "error": str(e)
            }
    
    return {
        "id": q_id,
        "topic": topic,
        "question": question,
        "answer": "",
        "latency": 0,
        "status": "ERROR",
        "error": "Max retries exceeded"
    }

def generate_report(results):
    latencies = [r["latency"] for r in results if r["latency"] > 0]
    avg_latency = statistics.mean(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    fallback_count = sum(1 for r in results if r["status"] == "FALLBACK")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    total = len(results)
    
    report = f"""# Client Performance & Gap Analysis Report

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions Tested:** {total}

## 1. Executive Summary
The RAG Chatbot was stress-tested with **1000 diverse queries** covering Policy, Locations, Fixtures, and Events.
- **Success Rate:** {success_count}/{total} ({(success_count/total)*100:.1f}%)
- **Data Gaps (Fallback):** {fallback_count}/{total} ({(fallback_count/total)*100:.1f}%)
- **System Stability:** {100 - (error_count/total)*100:.1f}% Error Free

## 2. Latency Performance
| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Average Response Time** | `{avg_latency:.2f}s` | Optimal is < 2.0s |
| **Max Response Time** | `{max_latency:.2f}s` | Peak load outlier |
| **Min Response Time** | `{min_latency:.2f}s` | Cached/Simple query |

## 3. Data Coverage & Gap Analysis
We categorized questions by topic to identify where the knowledge base is strong vs. weak.

| Topic | Total | Success | Fallback | Success % |
| :--- | :--- | :--- | :--- | :--- |
"""
    
    topics = sorted(list(set(r["topic"] for r in results)))
    for topic in topics:
        topic_results = [r for r in results if r["topic"] == topic]
        t_total = len(topic_results)
        t_success = sum(1 for r in topic_results if r["status"] == "SUCCESS")
        t_fallback = sum(1 for r in topic_results if r["status"] == "FALLBACK")
        succ_pct = (t_success / t_total) * 100 if t_total > 0 else 0
        report += f"| {topic} | {t_total} | {t_success} | {t_fallback} | {succ_pct:.1f}% |\n"

    report += """
## 4. Recommendations for Client
Based on the fallback rates, we recommend providing additional data in these areas:

1.  **Fixtures / Schedules (if low success):** Ensure all match IDs and team pairings are explicitly listed in the source documents. Queries like "Who is playing in Match ID 123" failed where ID metadata was missing.
2.  **Specific Events:** Detailed signals for 'Athletics' or specific sports rules were sometimes missing.
3.  **Policy Details:** Check coverage for niche policy questions (e.g., specific age limits or reservation quotas) if failures occurred there.

## 5. Detailed Latency & Response Log
| QID | Topic | Latency | Status | Question | Answer |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    # Log ALL results
    for r in results:
         # Escape pipes in answer to prevent breaking markdown table
         safe_ans = r['answer'].replace("|", " ").replace("\n", " ")[:200]
         report += f"| {r['id']} | {r['topic']} | {r['latency']}s | {r['status']} | {r['question']} | {safe_ans} |\n"
            
    return report

def main():
    print(f"Loading dataset from {INPUT_FILE}...")
    with open(INPUT_FILE, "r") as f:
        questions = json.load(f)
        
    # Full run - no slicing
    # questions = questions[:200] 
        
    print(f"🚀 Starting Stress Test for {len(questions)} questions (Sequential/Low Concurrency to avoid Ban)...")
    results = []
    
    # Use ThreadPool but with enforced delays to prevent 429/Abuse detection
    # Google Free Tier allows ~60 requests/min. 
    # Global limit might be higher but burst is dangerous.
    # We will simply run sequentially or with very strict rate limiting.
    
    # For safety: Run SEQUENTIALLY with delay. 
    # Concurrency was the cause of the ban.
    
    for i, q in enumerate(questions):
        res = ask_api(q)
        results.append(res)
        
        # Rate Limit: Groq Free Tier is strict (~30 RPM). 
        # 2.0s sleep + latency ensure we stay below limit.
        time.sleep(2.0) 
        
        if (i + 1) % 10 == 0:
            print(f"   Progress: {i + 1}/{len(questions)} done...")
            
    # Commented out concurrent execution to prevent "Abusive Activity" flag
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     futures = {executor.submit(ask_api, q): q for q in questions}
    #     completed = 0
    #     for future in futures:
    #         res = future.result()
    #         results.append(res)
    #         completed += 1
    #         if completed % 50 == 0:
    #             print(f"   Progress: {completed}/{len(questions)} done...")
        
    print("Generating report...")
    report_content = generate_report(results)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
