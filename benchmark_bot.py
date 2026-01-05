import requests
import json
import csv
import time
import asyncio
import aiohttp
from datetime import datetime

API_URL = "http://localhost:8000/chat"
INPUT_FILE = "data/training_questions_500.txt"
OUTPUT_FILE = "data/benchmark_results.csv"

async def fetch_response(session, question_id, question_text):
    start_time = time.time()
    try:
        async with session.post(API_URL, json={"query": question_text}) as response:
            latency = time.time() - start_time
            if response.status == 200:
                data = await response.json()
                res_content = data.get("response", "")
                source = data.get("source", "unknown")
                model = data.get("model_used", "unknown")
                
                # Determine Fallback Type based on response text
                fallback_type = "Success"
                if "official documents available" in res_content:
                    fallback_type = "Type 1: Absence"
                elif "I only have information for" in res_content:
                    fallback_type = "Type 2: Mismatch"
                elif "interpreted in a few ways" in res_content:
                    fallback_type = "Type 3: Ambiguous"
                elif "outside the scope" in res_content or "related to Sports" in res_content:
                    fallback_type = "Type 4: OutOfScope"
                elif "I don't have that information" in res_content: # Old fallback check
                    fallback_type = "Generic Fallback"
                
                return {
                    "id": question_id,
                    "question": question_text,
                    "status": "200",
                    "latency": f"{latency:.2f}",
                    "fallback_type": fallback_type,
                    "source": source,
                    "model": model,
                    "response_snippet": res_content[:100].replace("\n", " ") + "..."
                }
            else:
                return {
                    "id": question_id,
                    "question": question_text,
                    "status": str(response.status),
                    "latency": f"{latency:.2f}",
                    "fallback_type": "API Error",
                    "source": "error",
                    "model": "error",
                    "response_snippet": "Error"
                }
    except Exception as e:
         return {
            "id": question_id,
            "question": question_text,
            "status": "Exception",
            "latency": "0.00",
            "fallback_type": "Connection Error",
            "source": "error",
            "model": "error",
            "response_snippet": str(e)
        }

async def run_benchmark():
    # Read Questions
    questions = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("###"):
                # Clean line (remove numbering)
                parts = line.split(".", 1)
                if len(parts) > 1:
                    q_text = parts[1].strip()
                    q_id = parts[0].strip()
                    questions.append((q_id, q_text))
    
    print(f"🚀 Starting Benchmark for {len(questions)} questions...")
    
    results = []
    # Process in batches to respect rate limits (e.g., 5 concurrent)
    batch_size = 5
    
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(questions), batch_size):
            batch = questions[i:i+batch_size]
            tasks = [fetch_response(session, q[0], q[1]) for q in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            print(f"✅ Processed {min(i+batch_size, len(questions))}/{len(questions)}")
            await asyncio.sleep(1) # Gentle throttling

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "question", "status", "latency", "fallback_type", "source", "model", "response_snippet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for res in results:
            writer.writerow(res)
            
    print(f"🎉 Benchmark Complete! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
