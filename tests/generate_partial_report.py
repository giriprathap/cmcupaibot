import json
import statistics
import time
import os

JSONL_FILE = "tests/benchmark_results_5000.jsonl"
OUTPUT_FILE = "tests/benchmark_report_partial.md"

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
    
    report = f"""# Partial Benchmark Report (Post-Cancellation)

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
         report += f"- **[{r['id']}]** Q: {r['question']} | A: *{str(r['answer']).replace(chr(10), ' ')[:200]}...* (Source: {r['source']})\n"

    report += "\n## Detailed Results\n"
    report += "| ID | Question | Answer | Latency | Source |\n"
    report += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for r in results:
        # Sanitize answer for markdown table (remove newlines, limit length)
        safe_answer = str(r['answer']).replace('\n', ' ').replace('|', '\|')[:300]
        if len(str(r['answer'])) > 300: safe_answer += "..."
        
        report += f"| {r['id']} | {r['question']} | {safe_answer} | {r['latency']}s | {r['source']} |\n"

    return report

def main():
    if not os.path.exists(JSONL_FILE):
        print(f"File {JSONL_FILE} not found.")
        return

    results = []
    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except: pass

    print(f"Loaded {len(results)} results.")
    report = generate_markdown_report(results)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report report generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
