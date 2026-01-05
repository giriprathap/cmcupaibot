
import sys
import os

# Create a mock query
query = "how i can register for cmcup"

try:
    from rag.chain import get_rag_chain
    from rag.retriever import get_retriever
    
    print(f"🔎 Testing Retrieval for: '{query}'")
    
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    print(f"\n📄 Retrieved {len(docs)} Documents:")
    for i, doc in enumerate(docs):
        print(f"\n--- [Doc {i+1}] Source: {doc.metadata.get('source', 'unknown')} ---")
        print(doc.page_content[:500] + "...") # Print first 500 chars

except Exception as e:
    print(f"❌ Error: {e}")
