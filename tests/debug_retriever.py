from rag.retriever import get_retriever
from langchain_core.documents import Document

def debug_retrieval(query):
    print(f"\n🔍 Debugging Retrieval for: '{query}'")
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        
        print(f"📊 Found {len(docs)} documents.")
        for i, doc in enumerate(docs):
            print(f"   [{i+1}] {doc.page_content[:150]}...")
            print(f"       Metadata: {doc.metadata}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_retrieval("Who is the CM of Telangana?")
    debug_retrieval("Telangana ka CM kaun hai?")
