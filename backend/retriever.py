import chromadb

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

embedding_fn = (
    SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="kb_docs",
    embedding_function=embedding_fn
)


def retrieve(query):

    result = collection.query(
        query_texts=[query],
        n_results=3
    )

    docs = result["documents"][0]

    return docs