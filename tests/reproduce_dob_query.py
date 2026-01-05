
import sys
import os
import datetime

# Add project root to path
sys.path.append(os.getcwd())

from rag.sql_agent import run_sql_agent

def test_query(query):
    print(f"\n--- Testing Query: '{query}' ---")
    response = run_sql_agent(query)
    print(f"Response: {response}")

if __name__ == "__main__":
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        sys.stderr = f
        test_query("i was born on 2008, please suggest some discliplanes")
