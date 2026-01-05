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
                data = response.json()
                # Parse new response format: {"response": "...", "model_used": "..."}
                answer = data.get("response", data.get("answer", ""))
                model = data.get("model_used", "Unknown")
                
                is_fallback = "I don't have that information" in answer
                status = "FALLBACK" if is_fallback else "SUCCESS"
                
                return {
                    "id": q_id,
                    "topic": topic,
                    "question": question,
                    "answer": answer,
                    "model": model,
                    "latency": latency,
                    "status": status,
                    "error": None
                }
            elif response.status_code == 429:
                print(f"⚠️ 429 Rate Limit. Sleeping 5s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(5) # OpenAI tier is usually more generous than Groq free
                continue
            else:
                return {
                    "id": q_id,
                    "topic": topic,
                    "question": question,
                    "answer": "",
                    "model": "Error",
                    "latency": latency,
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "id": q_id,
                "topic": topic,
                "question": question,
                "answer": "",
                "model": "Error",
                "latency": 0,
                "status": "ERROR",
                "error": str(e)
            }
    
    return {
        "id": q_id,
        "topic": topic,
        "question": question,
        "answer": "",
        "model": "Error",
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
    
    # Model Usage Stats
    models = [r["model"] for r in results if r["model"] != "Error"]
    unique_models = set(models)
    
    report = f"""# OpenAI 10-Question Verification Report

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions:** {total}
**Models Detected:** {", ".join(unique_models)}

## 1. Summary
- **Success Rate:** {success_count}/{total} ({(success_count/total)*100:.1f}%)
- **Data Gaps (Fallback):** {fallback_count}/{total} ({(fallback_count/total)*100:.1f}%)
- **Errors:** {error_count}
- **Average Latency:** {avg_latency:.2f}s

## 2. Detailed Log
| QID | Topic | Latency | Model | Status | Question | Answer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    # Log ALL results
    for r in results:
         # Escape pipes/newlines
         safe_ans = r['answer'].replace("|", " ").replace("\n", " ")[:200]
         report += f"| {r['id']} | {r['topic']} | {r['latency']}s | {r['model']} | {r['status']} | {r['question']} | {safe_ans} |\n"
            
    return report

def main():
    print(f"Loading dataset from {INPUT_FILE}...")
    with open(INPUT_FILE, "r") as f:
        questions = json.load(f)
        
    # Limit run to 10 questions for verification
    questions = questions[:10] 
        
    print(f"🚀 Starting OpenAI Verification Test for {len(questions)} questions...")
    results = []
    
    for i, q in enumerate(questions):
        res = ask_api(q)
        results.append(res)
        
        # Gentle Pacing
        time.sleep(1.0) 
        
        print(f"[{i + 1}/{len(questions)}] {res['status']} ({res['latency']}s) - Model: {res.get('model')}")
            
    print("Generating report...")
    report_content = generate_report(results)
    
    OUTPUT_FILE_QUICK = "tests/openai_10q_report.md"
    with open(OUTPUT_FILE_QUICK, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Report saved to {OUTPUT_FILE_QUICK}")

if __name__ == "__main__":
    main()
