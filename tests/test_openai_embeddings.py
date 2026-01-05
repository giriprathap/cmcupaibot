import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from qdrant_client.http.models import VectorParams, Distance

# Load env vars
load_dotenv()

def test_openai_embedding_connection():
    print("Testing OpenAI Embeddings Connection...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables.")
        return

    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=api_key
        )
        
        text = "This is a test sentence to check embedding dimensions."
        vector = embeddings.embed_query(text)
        
        dim = len(vector)
        print(f"✅ Embedding generated successfully.")
        print(f"📏 Vector Dimension: {dim}")
        
        if dim == 1536:
            print("✅ Dimension matches expected (1536).")
        else:
            print(f"❌ Dimension mismatch! Expected 1536, got {dim}.")
            
    except Exception as e:
        print(f"❌ Error during embedding generation: {e}")

if __name__ == "__main__":
    test_openai_embedding_connection()
