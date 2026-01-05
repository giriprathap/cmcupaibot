import requests
import json
import time
import re
import os
import statistics
import concurrent.futures
import random

INPUT_FILE = "data/training_questions_500.txt"
OUTPUT_FILE = "tests/benchmark_report_5000.md"
JSONL_FILE = "tests/benchmark_results_5000.jsonl"
API_URL = "http://127.0.0.1:8000/ask"

# Configuration
MULTIPLIER = 10  # 500 * 10 = 5000
MAX_WORKERS = 1  # Ultra-safe mode: Sequential execution
# Increased sleep to effectively prevent rate limit/ban
MIN_SLEEP = 1.0
MAX_SLEEP = 2.0

def parse_questions(file_path):
    questions = []
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []
        
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_topic = "General"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect Header (### Topic)
        if line.startswith("###"):
            current_topic = line.replace("###", "").strip()
            continue
            
        # Detect Question (1. question?)
        match = re.match(r"^\d+\.\s+(.*)", line)
        if match:
            question_text = match.group(1)
            questions.append({
                "question": question_text,
                "topic": current_topic
            })
    return questions

def ask_api(q_data, index):
    # Jitter sleep to avoid thundering herd on API
    time.sleep(random.uniform(MIN_SLEEP, MAX_SLEEP))
    
    question = q_data["question"]
    topic = q_data["topic"]
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json={"query": question}, timeout=70)
        latency = round(time.time() - start_time, 2)
        
        if response.status_code == 200:
            data = response.json()
            answer_raw = data.get("response", "")
            
            # Handle nested response if applicable
            if isinstance(answer_raw, dict):
                answer = answer_raw.get("response", "")
                model = answer_raw.get("model_used", data.get("model_used", "unknown"))
            else:
                answer = answer_raw
                model = data.get("model_used", "unknown")

            source = data.get("source", "unknown")
            
            status = "SUCCESS"
            if "don't have" in answer.lower() or "not available" in answer.lower():
                status = "FALLBACK"
            if "error" in answer.lower() or "apologize" in answer.lower():
                status = "ERROR"
            
            # Simple check if answer is effectively empty text
            if len(answer) < 5:
                status = "ERROR"

            result = {
                "id": index,
                "question": question,
                "topic": topic,
                "answer": answer,
                "latency": latency,
                "status": status,
                "source": source,
                "model": model
            }
            log_result(result)
            return result
        else:
             # HTTP Error (e.g. 500, 429)
             res = {
                "id": index,
                "question": question,
                "topic": topic,
                "answer": f"HTTP {response.status_code}: {response.text[:100]}",
                "latency": latency,
                "status": "ERROR",
                "source": "api_error",
                "model": "none"
            }
             log_result(res)
             return res
    except Exception as e:
        res = {
            "id": index,
            "question": question,
            "topic": topic,
            "answer": str(e),
            "latency": 0,
            "status": "ERROR",
            "source": "client_error",
            "model": "none"
        }
        log_result(res)
        return res

def log_result(result):
    try:
        with open(JSONL_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(result) + "\n")
    except Exception as e:
        print(f"Log Error: {e}")

def generate_markdown_report(results):
    total = len(results)
    if total == 0:
        return "# Benchmark Failed: No Results"
        
    success = sum(1 for r in results if r["status"] == "SUCCESS")
    fallback = sum(1 for r in results if r["status"] == "FALLBACK")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    latencies = [r["latency"] for r in results if r["latency"] > 0]
    avg_lat = statistics.mean(latencies) if latencies else 0
    max_lat = max(latencies) if latencies else 0
    min_lat = min(latencies) if latencies else 0
    
    report = f"""# 5000-Question Large Scale Benchmark Report

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions Executed:** {total}
**Model Configuration:** Gemini 2.5 Flash / GPT 5.2

## Executive Summary
- **Success Rate:** {success} / {total} ({(success/total)*100:.2f}%)
- **Fallback/Empty Rate:** {fallback} / {total} ({(fallback/total)*100:.2f}%)
- **Error Failure Rate:** {errors} / {total} ({(errors/total)*100:.2f}%)
- **Avg Latency:** {avg_lat:.2f}s
- **Latency Range:** {min_lat:.2f}s - {max_lat:.2f}s

## Topic Analysis
| Topic | Count | Success % | Avg Latency |
| :--- | :--- | :--- | :--- |
"""
    topics = sorted(list(set(r["topic"] for r in results)))
    for topic in topics:
        t_res = [r for r in results if r["topic"] == topic]
        t_tot = len(t_res)
        t_suc = sum(1 for r in t_res if r["status"] == "SUCCESS")
        t_lats = [r["latency"] for r in t_res]
        t_avg = statistics.mean(t_lats) if t_lats else 0
        pct = (t_suc/t_tot)*100 if t_tot else 0
        report += f"| {topic} | {t_tot} | {pct:.1f}% | {t_avg:.2f}s |\n"

    report += "\n## Sample Errors & Failures\n"
    failures = [r for r in results if r["status"] == "ERROR"]
    # Limit to first 20 failures to save space
    for r in failures[:20]:
         report += f"- **[{r['id']}]** Q: {r['question']} | A: *{r['answer'].replace(chr(10), ' ')[:200]}...* (Source: {r['source']})\n"

    return report

def main():
    # Reset JSONL
    if os.path.exists(JSONL_FILE):
        os.remove(JSONL_FILE)
        
    print(f"Loading Base Dataset: {INPUT_FILE}")
    base_questions = parse_questions(INPUT_FILE)
    print(f"Base Count: {len(base_questions)}")
    
    print(f"Inflating Dataset x{MULTIPLIER}...")
    questions = base_questions * MULTIPLIER
    # Shuffle to simulate random load pattern
    # random.shuffle(questions) # User might prefer sequential checking of repetition? 
    # Let's keep sequential chunks to analyze caching, or shuffle? 
    # User said "perform 5000 ques running of it".
    # I'll keep it sequential-ish (grouped by original topic) but effectively repeated.
    
    total_q = len(questions)
    print(f"Total Questions to Run: {total_q}")
    print(f"Using {MAX_WORKERS} Concurrent Workers with Random Sleep ({MIN_SLEEP}-{MAX_SLEEP}s)")
    
    results = []
    
    print("🚀 Starting Benchmark 5000...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Pass index for tracking
        future_to_q = {executor.submit(ask_api, q, i): i for i, q in enumerate(questions)}
        
        counter = 0
        for future in concurrent.futures.as_completed(future_to_q):
            counter += 1
            try:
                res = future.result()
                results.append(res)
                if counter % 50 == 0:
                    print(f"Progress: {counter}/{total_q} ({(counter/total_q)*100:.1f}%)")
            except Exception as e:
                print(f"Critical Worker Error: {e}")
                
    print("✅ Benchmark Complete. Generating Report...")
    report_content = generate_markdown_report(results)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Report Saved to: {OUTPUT_FILE}")
    print(f"Raw Results in: {JSONL_FILE}")

if __name__ == "__main__":
    main()
