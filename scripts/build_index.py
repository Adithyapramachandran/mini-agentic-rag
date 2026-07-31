import os
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

folder = "kb"

existing = collection.get()

if existing["ids"]:
    collection.delete(
        ids=existing["ids"]
    )

files = os.listdir(folder)

for i, file in enumerate(files):

    filepath = os.path.join(
        folder,
        file
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    collection.add(
        ids=[str(i)],
        documents=[text],
        metadatas=[
            {"source": file}
        ]
    )

print(
    f"Indexed {len(files)} documents successfully"
)