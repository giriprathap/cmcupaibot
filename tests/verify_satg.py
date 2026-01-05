from rag.retriever import get_retriever

def verify():
    retriever = get_retriever()
    
    print("🧪 Test 1: Verify Chat Support Response")
    docs_chat = retriever.invoke("Is there chat support?")
    found_chat = False
    expected_snippet = "Yes, I am a chat support assistant for SATG and I can help you with information about sports, tournament details, CM Cup 2025"
    
    for doc in docs_chat:
        print(f"   Resource: {doc.page_content[:100]}...")
        if expected_snippet in doc.page_content:
            print("   ✅ Found expected response snippet!")
            found_chat = True
            break
            
    print("\n🧪 Test 2: Verify SATG Acronym")
    docs_acronym = retriever.invoke("What is SATG?")
    found_acronym = False
    for doc in docs_acronym:
        if "SATG" in doc.page_content:
            print("   ✅ Found 'SATG' in retrieved content.")
            found_acronym = True
            break
            
    if found_chat and found_acronym:
        print("\n✅ ALL TESTS PASSED")
    else:
        print("\n❌ TESTS FAILED")
        if not found_chat: print("   - Chat support response missing/incorrect.")
        if not found_acronym: print("   - SATG acronym not found.")
        exit(1)

if __name__ == "__main__":
    verify()
