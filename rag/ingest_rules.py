
import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Configuration
PDF_DIR = r"data/new data/Discipline_Rules"
DB_PATH = "data/qdrant_db"
COLLECTION_NAME = "rag_knowledge_base_gemini" # Matching retriever.py

def ingest_rules():
    if not os.path.exists(PDF_DIR):
        print(f"❌ Directory not found: {PDF_DIR}")
        return

    print(f"📂 Scanning {PDF_DIR} for PDFs...")
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    
    if not pdf_files:
        print("ℹ️ No PDF files found.")
        return

    print(f"found {len(pdf_files)} PDFs.")

    all_splits = []
    
    # Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    for pdf_path in pdf_files:
        try:
            print(f"   Using PyPDFLoader for: {os.path.basename(pdf_path)}...")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            
            # Add metadata source
            for d in docs:
                d.metadata["source_type"] = "rule_book"
                d.metadata["file_name"] = os.path.basename(pdf_path)
            
            splits = text_splitter.split_documents(docs)
            all_splits.extend(splits)
            print(f"     -> {len(splits)} chunks.")
        except Exception as e:
            print(f"   ❌ Error processing {os.path.basename(pdf_path)}: {e}")

    if not all_splits:
        print("❌ No documents to ingest.")
        return

    print(f"🧠 Initializing Embeddings (Gemini)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print(f"💾 Ingesting {len(all_splits)} chunks into Qdrant ({DB_PATH})...")
    client = QdrantClient(path=DB_PATH)
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    
    vector_store.add_documents(documents=all_splits)
    print("✅ Rules Ingestion Complete!")

if __name__ == "__main__":
    ingest_rules()
