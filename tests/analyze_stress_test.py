
import pandas as pd
import os

RESULTS_FILE = r"tests/stress_test_results_2000.csv"
REPORT_FILE = r"tests/stress_test_report_2000.md"

def analyze():
    print("📊 Starting Analysis...")
    
    if not os.path.exists(RESULTS_FILE):
        print(f"❌ Results file not found: {RESULTS_FILE}")
        return

    df = pd.read_csv(RESULTS_FILE)
    total = len(df)
    if total == 0:
        print("❌ No results to analyze.")
        return

    # Metrics
    success_count = len(df[df['success'] == True])
    failure_count = total - success_count
    success_rate = (success_count / total) * 100
    
    avg_latency = df['latency_sec'].mean()
    
    # Sources
    sources = df['source'].value_counts()
    
    # Error Patterns
    errors = df[df['success'] == False]['error'].value_counts().head(5)
    
    # Generate Markdown Report
    report = f"""# Stress Test Report (2000 Questions Analysis)

**Total Queries Tested:** {total}
**Success Rate:** {success_rate:.2f}% ({success_count}/{total})
**Average Latency:** {avg_latency:.2f}s

## 🔍 Data Sources
{sources.to_markdown()}

## 🚨 Top Errors
{errors.to_markdown()}

## 📉 Failed Queries (Sample)
"""
    
    failed_samples = df[df['success'] == False].head(10)
    for _, row in failed_samples.iterrows():
        report += f"- **Query:** `{row['query']}`\n  - **Error:** {row['error']}\n"
        
    # Save Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"✅ Report generated: {REPORT_FILE}")
    print(report)

if __name__ == "__main__":
    analyze()
