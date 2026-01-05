import sys
import os
from dotenv import load_dotenv
from langchain_core.documents import Document

# Add root to path
sys.path.append(os.getcwd())

# Load env
load_dotenv()

# Import function
from ingestion.embed_store import create_vector_store

def test():
    print("Testing ingestion logic with dummy data...")
    docs = [Document(page_content="This is a test chunk for embedding validation.", metadata={"source": "test"})]
    try:
        create_vector_store(docs)
        print("✅ Debug ingestion success.")
    except Exception as e:
        print(f"❌ Debug ingestion failed: {e}")

if __name__ == "__main__":
    test()
