import os
import sys
from dotenv import load_dotenv

# Ensure we can import from rag
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.retriever import get_retriever

def test_retrieval(query):
    print(f"\n🔎 Testing Query: '{query}'")
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    if not docs:
        print("❌ No documents retrieved.")
        return

    print(f"✅ Retrieved {len(docs)} documents.")
    for i, doc in enumerate(docs[:3]):  # Show top 3
        print(f"--- Doc {i+1} ---")
        print(doc.page_content[:300].replace('\n', ' '))
        print("...")

if __name__ == "__main__":
    test_retrieval("games")
    test_retrieval("What is cmcup 2015")
