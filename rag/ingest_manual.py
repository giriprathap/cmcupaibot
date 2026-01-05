
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = r"tests/registration_info.txt"
DB_PATH = "data/qdrant_db"
COLLECTION_NAME = "rag_knowledge_base"

def ingest():
    if not os.path.exists(FILE_PATH):
        print(f"❌ File not found: {FILE_PATH}")
        return

    print(f"📄 Loading {FILE_PATH}...")
    loader = TextLoader(FILE_PATH)
    docs = loader.load()
    
    print(f"✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
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
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest()
