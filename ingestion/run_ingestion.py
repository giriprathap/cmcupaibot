import sys
import os
sys.path.append(os.getcwd())

from ingestion.chunking import chunk_documents
from ingestion.embed_store import create_vector_store 
from langchain_community.document_loaders import DirectoryLoader, TextLoader

def run_ingestion():
    print("=== STARTING INGESTION PIPELINE ===")
    
    # 1. Load Markdown Files
    # Ensure this path matches your folder name exactly!
    loader = DirectoryLoader(
        "data/mdFiles", 
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    
    raw_docs = loader.load()
    print(f"📂 Loaded {len(raw_docs)} documents.")

    if not raw_docs:
        print("⚠️ No documents found. Check your 'data/mdFiles' folder!")
        return

    # 2. Chunk
    chunks = chunk_documents(raw_docs)

    # 3. Embed & Store
    create_vector_store(chunks)
    
    print("=== PIPELINE FINISHED ===")

if __name__ == "__main__":
    run_ingestion()