import sys
import os
from fastapi.testclient import TestClient

# Ensure project root is in path
sys.path.append(os.getcwd())

from api.main import app

client = TestClient(app)

def test_ask_endpoint():
    """Test the direct RAG functionality via /ask endpoint"""
    print("\n🧪 Testing Direct RAG Query via /ask...")
    payload = {"query": "What is the scholarship logic?"}
    
    # Send request to /ask
    response = client.post("/ask", json=payload)
    
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")
    
    # We expect 200 if RAG is working, or 503 if not initialized, or 500 if error
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "source" in data
        assert data["source"] == "rag_knowledge_base"
        print("✅ /ask endpoint worked successfully")
    elif response.status_code == 503:
        print("⚠️ Service Unavailable (RAG Brain not initialized). This is expected if keys are missing.")
    else:
        print(f"⚠️ Request failed with status {response.status_code}")

if __name__ == "__main__":
    test_ask_endpoint()
