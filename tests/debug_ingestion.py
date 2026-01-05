import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def test_embedding():
    print("Testing Embedding API...")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found.")
            return

        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vec = embeddings.embed_query("Hello world")
        print(f"✅ Embedding successful! Vector length: {len(vec)}")
    except Exception as e:
        print(f"❌ Embedding failed: {e}")

if __name__ == "__main__":
    test_embedding()
