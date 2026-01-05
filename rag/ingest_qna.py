
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = r"data/rag qna.txt"
DB_PATH = "data/qdrant_db"
COLLECTION_NAME = "rag_knowledge_base"

def ingest():
    if not os.path.exists(FILE_PATH):
        print(f"❌ File not found: {FILE_PATH}")
        return

    print(f"📄 Loading {FILE_PATH}...")
    try:
        loader = TextLoader(FILE_PATH, encoding="utf-8")
        docs = loader.load()
    except Exception as e:
        print(f"⚠️ UTF-8 failed ({e}), trying latin-1...")
        loader = TextLoader(FILE_PATH, encoding="latin-1")
        docs = loader.load()
    
    print(f"✂️ Splitting documents...")
    # Using a slightly larger chunk size to keep Q&A pairs together
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
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
