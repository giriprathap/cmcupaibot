import asyncio
import uuid
import os
import sys

sys.path.append(os.getcwd())
from api.main import chat_endpoint, ChatRequest

async def verify_memory():
    session = str(uuid.uuid4())
    print(f"Testing Session Memory (ID: {session})")
    
    # Q1: Set Context
    q1 = "Where is the Football match?"
    print(f"\nUser: {q1}")
    req1 = ChatRequest(query=q1, session_id=session)
    res1 = await chat_endpoint(req1)
    ans1 = res1.get('response')
    print(f"AI: {ans1}")
    
    # Q2: Recall (Pronoun Resolution)
    q2 = "When does it start?"
    print(f"\nUser: {q2}")
    req2 = ChatRequest(query=q2, session_id=session)
    res2 = await chat_endpoint(req2)
    ans2 = res2.get('response')
    print(f"AI: {ans2}")
    
    if "04:20" in ans2 or "time" in ans2 or "schedule" in ans2.lower(): 
        print("\n✅ Memory Test PAST: Pronoun 'it' resolved to Football!")
    else:
        print("\n❌ Memory Test FAILED: Context lost.")

if __name__ == "__main__":
    asyncio.run(verify_memory())
