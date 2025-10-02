import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.database_service import get_chroma_client, get_chroma_collection
from utils.pdf_utils import store_documents_in_collection


def ingest_documents():
    """
    Loads documents from the 'data' directory, splits them into chunks,
    creates embeddings, and saves them to a FAISS vector store.
    This script creates a persistent ChromaDB vector store.
    """
    data_dir = os.path.join(os.getcwd(), "data")

    # 1. Load Documents
    all_documents = []
    pdf_files = list(Path(data_dir).rglob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{data_dir}'.")
        return

    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = pdf_file.name
            doc.metadata["page"] = doc.metadata.get("page", 0) + 1
        all_documents.extend(docs)
    print(f"Loaded {len(all_documents)} pages from {len(pdf_files)} PDF files.")

    # 2. Chunk Documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len, add_start_index=True
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"Created {len(chunks)} chunks from {len(all_documents)} pages.")

    # 3. Store in ChromaDB
    client = get_chroma_client(directory=os.getenv("CHROMA_DB_DIR", "vector_store/chroma_db"))
    collection = get_chroma_collection(client)
    store_status = store_documents_in_collection(collection, chunks)

    if store_status:
        print("Documents stored successfully.")
    else:
        print("Failed to store documents.")

if __name__ == "__main__":
    ingest_documents()
