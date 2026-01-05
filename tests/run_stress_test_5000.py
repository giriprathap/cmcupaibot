import requests
import json
import time
import statistics
import os
import csv
import argparse

INPUT_FILE = "data/dataset_5000_multilingual.json"
RESULTS_FILE = "tests/stress_test_results_5000.csv"
REPORT_FILE = "tests/stress_test_report_5000.md"
API_URL = "http://127.0.0.1:8000/ask"
RATE_LIMIT_DELAY = 2.0  # Seconds

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
                answer = data.get("response", data.get("answer", ""))
                model_used = data.get("model_used", "Unknown")
                
                # Determine status
                is_fallback = "I don't have that information" in answer or "I'm sorry" in answer or "does not provide" in answer
                status = "FALLBACK" if is_fallback else "SUCCESS"
                
                return {
                    "id": q_id,
                    "topic": topic,
                    "language": language,
                    "question": question,
                    "answer": answer.replace("\n", " ")[:500], # Trucate for CSV
                    "model": model_used,
                    "latency": latency,
                    "status": status,
                    "error": ""
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

def load_existing_results():
    if not os.path.exists(RESULTS_FILE):
        return {}
    
    existing = {}
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing[int(row["id"])] = row
    return existing

def save_result(result, is_new_file=False):
    fieldnames = ["id", "topic", "language", "status", "latency", "model", "question", "answer", "error"]
    mode = "w" if is_new_file else "a"
    
    with open(RESULTS_FILE, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new_file:
            writer.writeheader()
        else:
            writer.writerow(result)

def generate_report(results_dict):
    results = list(results_dict.values())
    
    latencies = [float(r["latency"]) for r in results if float(r["latency"]) > 0]
    avg_latency = statistics.mean(latencies) if latencies else 0
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    fallback_count = sum(1 for r in results if r["status"] == "FALLBACK")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    total = len(results)
    
    report = f"""# 5000 Question Multilingual Stress Test Report

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions:** {total}

## 1. Executive Summary
- **Success Rate:** {success_count}/{total} ({(success_count/total)*100 if total else 0:.1f}%)
- **Data Gaps (Fallback):** {fallback_count}/{total} ({(fallback_count/total)*100 if total else 0:.1f}%)
- **Errors:** {error_count}/{total} ({(error_count/total)*100 if total else 0:.1f}%)
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
        
        l_latencies = [float(r["latency"]) for r in l_results if float(r["latency"]) > 0]
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

    return report

def main():
    parser = argparse.ArgumentParser(description="Run 5000 Q stress test")
    parser.add_argument("--limit", type=int, help="Limit number of questions to run (for testing)", default=0)
    args = parser.parse_args()

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file {INPUT_FILE} not found.")
        return

    print(f"Loading dataset from {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        all_questions = json.load(f)
        
    existing_results = load_existing_results()
    print(f"📊 Loaded {len(existing_results)} existing results.")
    
    # Filter out already answered questions
    questions_to_ask = [q for q in all_questions if q["id"] not in existing_results]
    
    if args.limit > 0:
        questions_to_ask = questions_to_ask[:args.limit]
        print(f"⚠️ LIMITING run to {args.limit} questions.")

    print(f"🚀 Starting Stress Test for {len(questions_to_ask)} questions...")
    print(f"   Rate Limit Delay: {RATE_LIMIT_DELAY}s")
    
    # Initialize CSV if not exists or empty
    if not os.path.exists(RESULTS_FILE) or os.stat(RESULTS_FILE).st_size == 0:
        save_result({}, is_new_file=True)

    count = 0
    try:
        for i, q in enumerate(questions_to_ask):
            print(f"[{i+1}/{len(questions_to_ask)}] (ID: {q['id']}) {q['language']}: {q['question']}")
            
            res = ask_api(q)
            save_result(res)
            existing_results[q["id"]] = res # Update in-memory for report
            
            count += 1
            if count % 10 == 0:
                print(f"   Saved progress ({count} done)")
            
            time.sleep(RATE_LIMIT_DELAY)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user. Generating partial report...")
    
    print("Generating final report...")
    report_content = generate_report(existing_results)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
