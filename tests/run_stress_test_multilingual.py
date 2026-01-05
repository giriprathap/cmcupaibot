import requests
import json
import time
import statistics
import os

INPUT_FILE = "data/dataset_multilingual_stress.json"
OUTPUT_FILE = "tests/stress_test_report_multilingual.md"
API_URL = "http://127.0.0.1:8000/ask"

def ask_api(question_data):
    q_id = question_data["id"]
    question = question_data["question"]
    topic = question_data["topic"]
    language = question_data.get("language", "English")
    
    max_retries = 3
    for attempt in range(max_retries):
        start_time = time.time()
        try:
            response = requests.post(API_URL, json={"query": question}, timeout=30)
            end_time = time.time()
            latency = round(end_time - start_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                # Handle possible response formats
                answer = data.get("response", data.get("answer", ""))
                model_used = data.get("model_used", "Unknown")
                
                is_fallback = "I don't have that information" in answer or "I'm sorry" in answer
                status = "FALLBACK" if is_fallback else "SUCCESS"
                
                return {
                    "id": q_id,
                    "topic": topic,
                    "language": language,
                    "question": question,
                    "answer": answer,
                    "model": model_used,
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
                    "language": language,
                    "question": question,
                    "answer": "",
                    "model": "None",
                    "latency": latency,
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "id": q_id,
                "topic": topic,
                "language": language,
                "question": question,
                "answer": "",
                "model": "None",
                "latency": 0,
                "status": "ERROR",
                "error": str(e)
            }
    
    return {
        "id": q_id,
        "topic": topic,
        "language": language,
        "question": question,
        "answer": "",
        "model": "None",
        "latency": 0,
        "status": "ERROR",
        "error": "Max retries exceeded"
    }

def generate_report(results):
    latencies = [r["latency"] for r in results if r["latency"] > 0]
    avg_latency = statistics.mean(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    fallback_count = sum(1 for r in results if r["status"] == "FALLBACK")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    total = len(results)
    
    report = f"""# Multilingual System Stress Test Report

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions:** {total}

## 1. Executive Summary
- **Success Rate:** {success_count}/{total} ({(success_count/total)*100:.1f}%)
- **Data Gaps (Fallback):** {fallback_count}/{total} ({(fallback_count/total)*100:.1f}%)
- **System Stability:** {100 - (error_count/total)*100:.1f}% Error Free
- **Avg Latency:** `{avg_latency:.2f}s`

## 2. Language Performance
| Language | Total | Success | Fallback | Success % | Avg Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    
    languages = sorted(list(set(r["language"] for r in results)))
    for lang in languages:
        l_results = [r for r in results if r["language"] == lang]
        l_total = len(l_results)
        l_success = sum(1 for r in l_results if r["status"] == "SUCCESS")
        l_fallback = sum(1 for r in l_results if r["status"] == "FALLBACK")
        l_succ_pct = (l_success / l_total) * 100 if l_total > 0 else 0
        
        l_latencies = [r["latency"] for r in l_results if r["latency"] > 0]
        l_avg_lat = statistics.mean(l_latencies) if l_latencies else 0
        
        report += f"| {lang} | {l_total} | {l_success} | {l_fallback} | {l_succ_pct:.1f}% | {l_avg_lat:.2f}s |\n"

    report += """
## 3. Topic Performance
| Topic | Total | Success | Fallback | Success % |
| :--- | :--- | :--- | :--- | :--- |
"""
    topics = sorted(list(set(r["topic"] for r in results)))
    for topic in topics:
        t_results = [r for r in results if r["topic"] == topic]
        t_total = len(t_results)
        t_success = sum(1 for r in t_results if r["status"] == "SUCCESS")
        t_fallback = sum(1 for r in t_results if r["status"] == "FALLBACK")
        t_succ_pct = (t_success / t_total) * 100 if t_total > 0 else 0
        report += f"| {topic} | {t_total} | {t_success} | {t_fallback} | {t_succ_pct:.1f}% |\n"

    report += """
## 4. Full Results Log
| ID | Lang | Topic | STS | Latency | Model | Question | Answer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for r in results:
         safe_ans = str(r['answer'] or "").replace("|", " ").replace("\n", " ")[:150]
         report += f"| {r['id']} | {r['language']} | {r['topic']} | {r['status']} | {r['latency']}s | {r['model']} | {r['question']} | {safe_ans} |\n"
            
    return report

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file {INPUT_FILE} not found.")
        return

    print(f"Loading dataset from {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"🚀 Starting Multilingual Stress Test for {len(questions)} questions...")
    results = []
    
    # SEQUENTIAL execution with forced delay to respect Rate Limits
    for i, q in enumerate(questions):
        print(f"[{i+1}/{len(questions)}] Asking ({q['language']}): {q['question']}...")
        res = ask_api(q)
        results.append(res)
        
        # 2 Second Delay between requests
        # OpenAI/Groq limits are often RPM based. 2s = 30 RPM max, which is safe.
        time.sleep(2.0)
        
    print("Generating report...")
    report_content = generate_report(results)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
