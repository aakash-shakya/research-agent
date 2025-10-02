def store_documents_in_collection(collection, chunks):
    """
    Stores documents in the specified ChromaDB collection with embeddings.
    """
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

    return True