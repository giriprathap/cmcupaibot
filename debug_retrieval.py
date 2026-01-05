from rag.retriever import get_retriever
from dotenv import load_dotenv

load_dotenv()

def debug():
    print("🔍 Testing Retriever...")
    retriever = get_retriever()
    
    query = "Allipalli"
    print(f"\nQuery: {query}")
    docs = retriever.invoke(query)
    
    print(f"Found {len(docs)} docs.")
    for i, doc in enumerate(docs):
        print(f"[{i}] {doc.page_content[:200]}...")

if __name__ == "__main__":
    debug()
