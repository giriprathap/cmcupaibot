import sys
import os

# Add root to python path to find 'rag' module
sys.path.append(os.getcwd())

from rag.retriever import get_retriever

def test_retrieval():
    print("Testing Retrieval...")
    try:
        retriever = get_retriever()
        query = "What is the sports policy of Telangana?"
        docs = retriever.invoke(query)
        
        print(f"✅ Retrieved {len(docs)} documents.")
        if len(docs) > 0:
            print("First document content snippet:")
            print(docs[0].page_content[:200])
        else:
            print("❌ No documents retrieved.")
            
    except Exception as e:
        print(f"❌ Error during retrieval: {e}")

if __name__ == "__main__":
    test_retrieval()
