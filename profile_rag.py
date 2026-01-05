
import time
import os
from rag.retriever import get_retriever
from rag.llm_manager import ask_llm

def profile_rag():
    print("Starting RAG Profiling...")
    
    # 1. Profile Embedding/Retriever Setup
    start = time.time()
    retriever = get_retriever()
    print(f"[Profiling] Retriever Init: {time.time() - start:.2f}s")
    
    query = "what is cmcup"
    
    # 2. Profile Retrieval
    start = time.time()
    docs = retriever.invoke(query)
    print(f"[Profiling] Retrieval (Search): {time.time() - start:.2f}s")
    print(f"  - Retrieved {len(docs)} documents")
    
    context = "\n".join([d.page_content for d in docs])
    
    # 3. Profile LLM
    start = time.time()
    print("[Profiling] Calling LLM...")
    response = ask_llm(context, query)
    print(f"[Profiling] LLM Response Time: {time.time() - start:.2f}s")
    print(f"  - Model Used: {response.get('model_used')}")
    print(f"  - Response Preview: {response.get('response')[:50]}...")

if __name__ == "__main__":
    profile_rag()
