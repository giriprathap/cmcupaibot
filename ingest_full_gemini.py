import os
import glob
from langchain_community.document_loaders import TextLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

def ingest_all():
    print("🚀 Starting Full Ingestion with Gemini Embeddings...")
    
    docs = []
    
    # 1. Load Standard RAG QnA
    qna_path = "data/rag qna.txt"
    if os.path.exists(qna_path):
        print(f"📄 Loading {qna_path}...")
        loader = TextLoader(qna_path, encoding='utf-8')
        docs.extend(loader.load())
        
    # 2. Load New Data Folder
    new_data_dir = "data/new data"
    files = glob.glob(os.path.join(new_data_dir, "*"))
    print(f"📂 Found {len(files)} files in {new_data_dir}")
    
    for file_path in files:
        print(f"   - Loading {file_path}...")
        try:
            if file_path.endswith(".txt"):
                loader = TextLoader(file_path, encoding='utf-8')
                docs.extend(loader.load())
            elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                try:
                    loader = UnstructuredExcelLoader(file_path)
                    docs.extend(loader.load())
                except Exception as e:
                    print(f"     ⚠️ Excel Load Error: {e}")
            else:
                print(f"     ⚠️ Skipped unsupported file type: {file_path}")
        except Exception as e:
            print(f"     ❌ Failed to load {file_path}: {e}")

    # 3. Load Generated MD Files (SQL Data)
    md_dir = "data/mdFiles"
    if os.path.exists(md_dir):
        md_files = glob.glob(os.path.join(md_dir, "*.md"))
        print(f"📂 Found {len(md_files)} markdown files in {md_dir}")
        for file_path in md_files:
            print(f"   - Loading {file_path}...")
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs.extend(loader.load())
            except Exception as e:
                print(f"     ❌ Failed to load {file_path}: {e}")

    # 3. Split
    print(f"✂️ Splitting {len(docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"   -> Created {len(splits)} chunks.")
    
    # 4. Ingest
    print("🧠 Initializing Gemini Embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    print("💾 Ingesting into Qdrant (rag_knowledge_base_gemini)...")
    client = QdrantClient(path="data/qdrant_db")
    
    # Manual Recreation
    print("   -> Recreating Collection...")
    if client.collection_exists("rag_knowledge_base_gemini"):
        client.delete_collection("rag_knowledge_base_gemini")
        
    client.create_collection(
        collection_name="rag_knowledge_base_gemini",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    
    # Add Documents
    print("   -> Adding documents...")
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag_knowledge_base_gemini",
        embedding=embeddings,
    )
    vector_store.add_documents(splits)
    
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest_all()
