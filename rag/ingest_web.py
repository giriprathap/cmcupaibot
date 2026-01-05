
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# URLs to scrape
URLS = [
    "https://satg.telangana.gov.in/",
    "https://satg.telangana.gov.in/cmcup",
    # Add other key pages here if discoverable or standard
]

DB_PATH = "data/qdrant_db"
COLLECTION_NAME = "rag_knowledge_base"

def ingest_web():
    print(f"🌐 Scrappig URLs: {URLS}")
    
    # WebBaseLoader uses BeautifulSoup under the hood
    loader = WebBaseLoader(URLS)
    docs = loader.load()
    print(f"   -> Loaded {len(docs)} pages.")
    
    print(f"✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    print(f"   -> Created {len(splits)} chunks.")
    
    print("🧠 Initializing Embeddings (OpenAI)...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    print(f"💾 Ingesting into Qdrant ({DB_PATH})...")
    client = QdrantClient(path=DB_PATH)
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    
    vector_store.add_documents(documents=splits)
    print("✅ Web Ingestion Complete!")

if __name__ == "__main__":
    ingest_web()
