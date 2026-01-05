import requests
import json
import time
import re
import os
import statistics
import concurrent.futures

INPUT_FILE = "data/training_questions_500.txt"
OUTPUT_FILE = "tests/benchmark_report_500.md"
API_URL = "http://127.0.0.1:8000/ask"

def parse_questions(file_path):
    questions = []
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

def ask_api(q_data):
    question = q_data["question"]
    topic = q_data["topic"]
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json={"query": question}, timeout=60)
        latency = round(time.time() - start_time, 2)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "")
            source = data.get("source", "unknown")
            model = data.get("model_used", "unknown")
            
            # Simple fallback detection
            status = "SUCCESS"
            if "don't have" in answer.lower() or "not available" in answer.lower():
                status = "FALLBACK"
            if "error" in answer.lower():
                status = "ERROR"
                
            result = {
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
             res = {
                "question": question,
                "topic": topic,
                "answer": f"HTTP {response.status_code}",
                "latency": latency,
                "status": "ERROR",
                "source": "api_error",
                "model": "none"
            }
             log_result(res)
             return res
    except Exception as e:
        res = {
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
    with open("tests/benchmark_results_500.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

def generate_markdown_report_from_file():
    results = []
    if not os.path.exists("tests/benchmark_results_500.jsonl"):
        return "No results found."
        
    with open("tests/benchmark_results_500.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line[:50]}...")
    
    return generate_markdown_report(results)

def main():
    # Clear previous results
    if os.path.exists("tests/benchmark_results_500.jsonl"):
        os.remove("tests/benchmark_results_500.jsonl")

    print(f"Parsing questions from {INPUT_FILE}...")
    total = len(results)
    success = sum(1 for r in results if r["status"] == "SUCCESS")
    fallback = sum(1 for r in results if r["status"] == "FALLBACK")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    
    latencies = [r["latency"] for r in results if r["latency"] > 0]
    avg_lat = statistics.mean(latencies) if latencies else 0
    max_lat = max(latencies) if latencies else 0
    
    report = f"""# 500-Question Benchmark Report (Gemini 2.5 Flash / GPT 5.2 Pro)

**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Total Questions:** {total}
**Model Target:** Gemini 2.5 Flash / GPT 5.2 Pro

## Summary
- **Success Rate:** {success}/{total} ({(success/total)*100:.1f}%)
- **Fallback Rate:** {fallback}/{total} ({(fallback/total)*100:.1f}%)
- **Error Rate:** {errors}/{total} ({(errors/total)*100:.1f}%)
- **Avg Latency:** {avg_lat:.2f}s
- **Max Latency:** {max_lat:.2f}s

## Detailed Gap Analysis by Topic
| Topic | Total | Success | Fallback | Success % |
| :--- | :--- | :--- | :--- | :--- |
"""
    topics = sorted(list(set(r["topic"] for r in results)))
    for topic in topics:
        t_res = [r for r in results if r["topic"] == topic]
        t_tot = len(t_res)
        t_suc = sum(1 for r in t_res if r["status"] == "SUCCESS")
        t_fal = sum(1 for r in t_res if r["status"] == "FALLBACK")
        pct = (t_suc/t_tot)*100 if t_tot else 0
        report += f"| {topic} | {t_tot} | {t_suc} | {t_fal} | {pct:.1f}% |\n"

    report += "\n## Failed/Fallback Queries (Actionable Insights)\n"
    for r in results:
        if r["status"] != "SUCCESS":
             report += f"- **[{r['topic']}]** {r['question']} -> *{r['answer'].replace(chr(10), ' ')}*\n"

    return report

def main():
    print(f"Parsing questions from {INPUT_FILE}...")
    questions = parse_questions(INPUT_FILE)
    print(f"Loaded {len(questions)} questions.")
    
    # ---------------------------------------------------------
    # LIMIT FOR DEMO/SPEED if needed, but user asked for ALL 500
    # questions = questions[:10] 
    # ---------------------------------------------------------
    
    results = []
    print("Starting benchmark (Sequential to avoid rate limits)...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_q = {executor.submit(ask_api, q): q for q in questions}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_q)):
            try:
                future.result() # We log inside ask_api
                if (i+1) % 10 == 0:
                    print(f"Processed {i+1}/{len(questions)}...")
            except Exception as e:
                print(f"Result Error: {e}")
                
    print("Generating report...")
    report = generate_markdown_report_from_file()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
