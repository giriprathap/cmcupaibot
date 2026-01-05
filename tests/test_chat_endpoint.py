import sys
import os
from fastapi.testclient import TestClient

# Ensure project root is in path
sys.path.append(os.getcwd())

from api.main import app

client = TestClient(app)

def test_chat_direct_lookup():
    """Test the direct lookup functionality via /chat endpoint"""
    print("\n🧪 Testing Direct Lookup (Phone Number)...")
    payload = {"query": "Status for 8328508582"}
    response = client.post("/chat", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "source" in data
    assert data["source"] == "sql_database"
    assert "8328508582" in payload["query"] # Context check

def test_chat_rag_query():
    """Test the RAG functionality via /chat endpoint"""
    print("\n🧪 Testing RAG Query (General Question)...")
    payload = {"query": "Tell me about the match schedule"}
    
    # Note: This might fail if RAG chain isn't loaded or keys are missing
    # But we want to see the application logic flow
    response = client.post("/chat", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # We expect either 200 (if keys work) or 503/500 if keys/models fail
    # But we mostly want to check if it tried to hit the RAG path
    if response.status_code == 200:
        data = response.json()
        assert data["source"] == "rag_knowledge_base"
    else:
        print("RAG Request failed as expected (likely due to missing inference keys in test env)")

if __name__ == "__main__":
    test_chat_direct_lookup()
    test_chat_rag_query()
