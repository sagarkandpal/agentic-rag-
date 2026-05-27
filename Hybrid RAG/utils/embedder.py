#we have downloaded this mini llm model to create our embeddings because without it it is taking so much time
#because it is calling api for creating embeddings and showing rate limit - 10sec.

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Embedding function
def get_embedding(text: str):
    return model.encode(text).tolist()