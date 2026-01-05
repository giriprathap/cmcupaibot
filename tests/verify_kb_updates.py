from rag.retriever import get_retriever

def verify():
    retriever = get_retriever()
    
    queries = [
        "Where to register online?",
        "Can I register from my phone?",
        "Where is my match venue?",
        "When will matches start?",
        "Is there any helpline number?",
        "Any safety issues reported?",
        "How many volunteers deployed?"
    ]
    
    print("--- Verifying KB Updates ---\n")
    
    for q in queries:
        print(f"Q: {q}")
        docs = retriever.invoke(q)
        # Just print the first 100 chars of top doc to verify signal
        if docs:
            print(f"A: {docs[0].page_content[:150]}...\n")
        else:
            print("A: NO RESPONSE FOUND\n")

if __name__ == "__main__":
    verify()
