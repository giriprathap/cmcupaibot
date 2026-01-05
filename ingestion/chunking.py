from typing import List
from langchain_core.documents import Document
# UPDATED IMPORT:
from langchain_text_splitters import RecursiveCharacterTextSplitter 

def chunk_documents(docs: List[Document]) -> List[Document]:
    print(f"✂️  Chunking {len(docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(docs)
    print(f"   ➡ Created {len(chunks)} chunks.")
    return chunks