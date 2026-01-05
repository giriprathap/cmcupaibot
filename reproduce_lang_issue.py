from rag.llm_manager import ask_llm
from rag.retriever import get_retriever

def reproduce():
    query = "When is CM CUP starting?"
    print(f"Query: {query}")
           
    # 1. Get Context (Simulate what RAG does)
    retriever = get_retriever()
    docs = retriever.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # 2. Ask LLM
    print("\n--- Sending to LLM ---")
    result = ask_llm(context, query)
    print("\n--- LLM Response ---")
    print(result['response'])
    print(f"Model: {result['model_used']}")

if __name__ == "__main__":
    reproduce()
