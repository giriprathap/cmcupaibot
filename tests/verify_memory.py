import asyncio
import uuid
import os
import sys

sys.path.append(os.getcwd())
from api.main import chat_endpoint, ChatRequest

async def verify_memory():
    session = str(uuid.uuid4())
    print(f"Testing Session Memory (ID: {session})")
    
    # Q1: Establish Context
    q1 = "Who is the Chief Minister of Telangana?"
    print(f"\nUser: {q1}")
    req1 = ChatRequest(query=q1, session_id=session)
    res1 = await chat_endpoint(req1)
    print(f"AI: {res1.get('response')}")
    
    # Q2: Follow-up relying on context ("He")
    q2 = "Which political party does he belong to?"
    print(f"\nUser: {q2}")
    req2 = ChatRequest(query=q2, session_id=session)
    res2 = await chat_endpoint(req2)
    ans2 = res2.get('response')
    print(f"AI: {ans2}")
    
    if "Congress" in ans2 or "Revanth" in ans2: 
        print("\n✅ Memory Test PAST: Context recognized!")
    else:
        print("\n❌ Memory Test FAILED: Context lost.")

if __name__ == "__main__":
    asyncio.run(verify_memory())
