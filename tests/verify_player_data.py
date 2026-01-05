from rag.retriever import get_retriever

def verify():
    retriever = get_retriever()
    
    # Test 1: General player query
    query = "Who are the players in Football?"
    print(f"\nQuerying: {query}")
    docs = retriever.invoke(query)
    
    print("\n--- Retrieved Documents (Football) ---")
    found_player = False
    for doc in docs:
        print(f"- {doc.page_content[:100]}...")
        if "Player **" in doc.page_content:
            found_player = True
            
    if found_player:
        print("✅ Found player data for Football!")
    else:
        print("❌ No player data found for Football.")

    # Test 2: Specific player name (from the snapshot seen earlier: Surugula Siddhartha)
    query_specific = "Details of Surugula Siddhartha"
    print(f"\nQuerying: {query_specific}")
    docs = retriever.invoke(query_specific)
    
    print("\n--- Retrieved Documents (Specific) ---")
    found_specific = False
    for doc in docs:
        if "Surugula Siddhartha" in doc.page_content:
            print(f"- {doc.page_content}")
            found_specific = True
            break
            
    if found_specific:
        print("✅ Found specific player data!")
    else:
        print("❌ Specific player data not found.")

if __name__ == "__main__":
    verify()
