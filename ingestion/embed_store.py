import os
import time
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def create_vector_store(chunks):
    print("🧠 Initializing Embeddings & Vector Store...")
    
    # 1. SWITCH TO OPENAI EMBEDDINGS
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 2. Setup Qdrant Client (Local)
    client = QdrantClient(path="data/qdrant_db")
    collection_name = "rag_knowledge_base"

    # 3. Create/Recreate Collection
    # text-embedding-3-small is 1536 dimensions
    print(f"📦 Creating/Recreating collection '{collection_name}'...")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

    print(f"🚀 Preparing to ingest {len(chunks)} chunks...")

    # 4. Init Vector Store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    # 5. Add Documents (BATCHED)
    try:
        batch_size = 50
        total_chunks = len(chunks)
        print(f"📦 Ingesting {total_chunks} chunks in batches of {batch_size}...")
        
        for i in range(0, total_chunks, batch_size):
            batch = chunks[i:i + batch_size]
            print(f"   ➡ Processing batch {i // batch_size + 1} ({len(batch)} chunks)...")
            
            vector_store.add_documents(documents=batch)
            
            # Gentle pacing
            time.sleep(1)
            
        print("✅ SUCCESS: All data processed!")
    except Exception as e:
        print(f"❌ Error adding documents: {e}")

    return vector_store