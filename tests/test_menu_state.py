import pytest
from fastapi.testclient import TestClient
# Import app after making sure sys.path is correct if needed, but TestClient handles it usually if package form is good.
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

client = TestClient(app)

def test_menu_flow():
    session_id = "test_session_001"
    
    # 1. Main Menu (Start)
    resp = client.post("/chat", json={"query": "Hi", "session_id": session_id})
    assert resp.status_code == 200
    data = resp.json()
    print(f"Response 1: {data['response']}")
    assert "Welcome to Telangana Sports Authority" in data["response"]
    assert "1️⃣ Player Registration" in data["response"]

    # 2. Navigate to Registration (Option 1)
    resp = client.post("/chat", json={"query": "1", "session_id": session_id})
    data = resp.json()
    print(f"Response 2: {data['response']}")
    assert "Player Registration & Venue" in data["response"]
    assert "1️⃣ Search by Phone Number" in data["response"]

    # 3. Sub-menu Navigation (Option 1 -> Search by Phone)
    resp = client.post("/chat", json={"query": "1", "session_id": session_id})
    data = resp.json()
    print(f"Response 3: {data['response']}")
    assert "Please enter your registered **Phone Number**" in data["response"]

    # 4. Back Navigation
    resp = client.post("/chat", json={"query": "Back", "session_id": session_id})
    data = resp.json()
    print(f"Response 4: {data['response']}")
    assert "Player Registration & Venue" in data["response"]  # Should go back to Reg menu
    
    # 5. Back to Main
    resp = client.post("/chat", json={"query": "Back", "session_id": session_id})
    data = resp.json()
    assert "Welcome to Telangana Sports Authority" in data["response"]

def test_unknown_input_in_menu():
    session_id = "test_session_002"
    # Start
    client.post("/chat", json={"query": "Hi", "session_id": session_id})
    
    # Invalid Option
    resp = client.post("/chat", json={"query": "99", "session_id": session_id})
    data = resp.json()
    # Should probably stay in menu or show error, but currently might fall through to RAG logic unless handled.
    # For this implementation, let's assume valid digits are caught, invalid might fall through or show invalid.
    # We'll check if it handles it gracefully.
