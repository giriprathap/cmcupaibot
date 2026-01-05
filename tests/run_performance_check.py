import asyncio
import os
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())

from api.main import chat_endpoint, ChatRequest

# Valid Questions
common_questions = [
    "How to join CM CUP?",
    "Where to register online?",
    "Can I register from my phone?",
    "My name missing after registration – what to do?",
    "When will matches start?",
    "Where to see schedule?",
    "Which sports are included?",
    "Do girls also play?",
    "Where is my match venue?",
    "Do winners get prizes?",
    "When will results come?",
    "How to get certificate?",
    "Website not opening – what to do?",
    "Is there any helpline number?",
    "Can I complain if issue happens?"
]

ias_questions = [
    "How many total participants registered?",
    "District-wise participation report available?",
    "Gender-wise breakup available?",
    "How many venues finalized?",
    "Any safety issues reported?",
    "Medical facilities arranged?",
    "How many volunteers deployed?",
    "Daily progress report available?",
    "Budget utilization status?",
    "Any incidents reported?"
]

async def run_tests():
    results = []
    
    print("Running Common User Questions...")
    for q in common_questions:
        print(f"Asking: {q}")
        try:
            resp = await chat_endpoint(ChatRequest(query=q))
            # Handle response type (might be dict or object depending on api implementation changes, 
            # currently dict based on previous reads)
            ans = resp.get("response", "No response")
            src = resp.get("source", "Unknown")
            model = resp.get("model_used", "Unknown")
            results.append(f"| {q} | {ans.replace('|', '-').replace(chr(10), '<br>')} | {src} |")
        except Exception as e:
            results.append(f"| {q} | ERROR: {str(e)} | ERROR |")

    print("Running IAS Questions...")
    for q in ias_questions:
        print(f"Asking: {q}")
        try:
            resp = await chat_endpoint(ChatRequest(query=q))
            ans = resp.get("response", "No response")
            src = resp.get("source", "Unknown")
            model = resp.get("model_used", "Unknown")
            results.append(f"| {q} | {ans.replace('|', '-').replace(chr(10), '<br>')} | {src} |")
        except Exception as e:
            results.append(f"| {q} | ERROR: {str(e)} | ERROR |")

    # Write Report
    with open("performance_results.md", "w", encoding="utf-8") as f:
        f.write("# Performance Check Results\n\n")
        f.write("| Question | Response | Source |\n")
        f.write("|----------|----------|--------|\n")
        f.write("\n".join(results))
    
    print("\n✅ Report generated: performance_results.md")

if __name__ == "__main__":
    asyncio.run(run_tests())
