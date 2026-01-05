from rag.retriever import get_retriever

def verify():
    retriever = get_retriever()
    # Query for Match 6 to see the format
    query = "details of Match 6"
    print(f"Querying: {query}")
    docs = retriever.invoke(query)
    
    print("\n--- Retrieved Documents ---")
    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1}:")
        print(doc.page_content)
        
    # Check if the desired format is present
    found = False
    for doc in docs:
        if "- **Match 6**" in doc.page_content:
            found = True
            print("\n✅ Found new list format!")
            break
            
    if not found:
        print("\n❌ Did not find new list format.")

if __name__ == "__main__":
    verify()
