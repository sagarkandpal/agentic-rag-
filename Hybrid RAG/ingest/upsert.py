from vectordb.pinecone_db import get_index
from utils.embedder import get_embedding
import time

index = get_index()

def upsert_documents(chunks):

    vectors = []

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        vectors.append({
            "id": str(i),
            "values": embedding,
            "metadata": {
                "text": chunk
            }
        })

    # Batch mein upsert karo (100 at a time)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"Uploaded {min(i + batch_size, len(vectors))}/{len(vectors)} chunks")
        time.sleep(1)

    print("Documents uploaded successfully!")