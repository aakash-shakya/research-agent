import chromadb
from chromadb.config import Settings

def get_chroma_client(directory: str="vector_store/chroma_db"):
    """
    Initializes and returns a ChromaDB client.
    """
    client = chromadb.PersistentClient(
        path=directory
    )
    return client

def get_chroma_collection(client, collection_name="research_agent_pdf_collection"):
    """
    Retrieves or creates a ChromaDB collection.
    """
    collection = client.get_or_create_collection(name=collection_name)
    return collection

def add_documents_to_collection(collection, documents):
    """
    Adds documents to the specified ChromaDB collection with embeddings.
    """
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    ids = [str(i) for i in range(len(documents))]
    
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(collection, query_text, n_results=5):
    """
    Queries the ChromaDB collection for similar documents.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results

def get_retriever_from_collection(collection, k=5):
    """
    Creates a retriever from the ChromaDB collection.
    """
    from langchain_community.vectorstores import Chroma
    from services.embedding_service import hf

    retriever = Chroma(
        collection_name=collection,
        embedding_function=hf
    ).as_retriever(search_kwargs={"k": k})
    return retriever