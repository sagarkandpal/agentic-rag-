# retriever/vector_retriever.py

from vectordb.pinecone_db import get_index
from utils.embedder import get_embedding

# Connect Pinecone
index = get_index()


def vector_search(query, top_k=3):

    # Convert query into embedding
    query_embedding = get_embedding(query)

    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Extract text
    docs = []

    for match in results["matches"]:
        docs.append(match["metadata"]["text"])

    return docs