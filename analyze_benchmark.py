import csv
import statistics
from collections import defaultdict, Counter

QUESTION_FILE = "data/training_questions_500.txt"
RESULTS_FILE = "data/benchmark_results.csv"
REPORT_FILE = r"C:\Users\Rishabh\.gemini\antigravity\brain\f4625e82-ee8a-43c4-ad20-c79773bdc192\benchmarking_report.md"

def load_categories():
    """Maps question text to category based on the training file headers."""
    q_map = {}
    current_category = "General"
    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("###"):
                current_category = line.replace("###", "").strip()
            elif line and line[0].isdigit():
                # Extract question text: "1. what is..." -> "what is..."
                parts = line.split(".", 1)
                if len(parts) > 1:
                    q_text = parts[1].strip()
                    q_map[q_text] = current_category
    return q_map

def analyze():
    print(f"📊 Analyzing {RESULTS_FILE}...")
    
    q_categories = load_categories()
    results = []
    
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
    except FileNotFoundError:
        print("❌ Results file not found yet.")
        return

    total = len(results)
    if total == 0:
        print("⚠️ No results to analyze.")
        return

    # Metrics
    latencies = [float(r["latency"]) for r in results]
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    
    # Outcomes
    outcomes = Counter([r["fallback_type"] for r in results])
    success_count = outcomes.get("Success", 0)
    success_rate = (success_count / total) * 100
    
    # Category Analysis
    cat_stats = defaultdict(lambda: {"total": 0, "success": 0, "failures": []})
    
    for r in results:
        q_text = r["question"]
        # Fuzzy match or exact match category
        cat = q_categories.get(q_text, "Unknown")
        
        cat_stats[cat]["total"] += 1
        if r["fallback_type"] == "Success":
            cat_stats[cat]["success"] += 1
        else:
            cat_stats[cat]["failures"].append(r)

    # Generate Report
    report = []
    report.append(f"# RAG Chatbot Benchmarking Report (GPT-4o)\n")
    report.append(f"**Date:** 2025-12-30\n")
    report.append(f"**Total Questions:** {total}\n")
    report.append(f"**Overall Success Rate:** {success_rate:.1f}%\n")
    report.append(f"**Average Latency:** {avg_latency:.2f}s\n")
    
    report.append(f"\n## 1. Outcome Distribution")
    report.append(f"| Outcome | Count | Percentage |")
    report.append(f"| :--- | :--- | :--- |")
    for k, v in outcomes.items():
        pct = (v / total) * 100
        report.append(f"| {k} | {v} | {pct:.1f}% |")

    report.append(f"\n## 2. Category Performance")
    report.append(f"| Category | Total | Success Rate | Weakness |")
    report.append(f"| :--- | :--- | :--- | :--- |")
    
    for cat, stats in sorted(cat_stats.items()):
        total_q = stats["total"]
        succ_rate = (stats["success"] / total_q) * 100 if total_q > 0 else 0
        weakness = "None"
        if succ_rate < 80:
            weakness = "HIGH"
        elif succ_rate < 90:
            weakness = "Moderate"
        report.append(f"| {cat} | {total_q} | {succ_rate:.1f}% | {weakness} |")

    report.append(f"\n## 3. Weakest Areas (Sample Failures)")
    for cat, stats in sorted(cat_stats.items()):
        if stats["failures"]:
            report.append(f"\n### {cat} (Failures: {len(stats['failures'])})")
            # Show top 3 failures
            for f in stats["failures"][:3]:
                report.append(f"*   **Q:** {f['question']}")
                report.append(f"    *   **Fallback:** {f['fallback_type']}")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"✅ Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    analyze()
