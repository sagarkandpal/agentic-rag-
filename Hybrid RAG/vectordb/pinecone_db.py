from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

# Connect to index
index = pc.Index("hybrid-rag")


# Function to get Pinecone index
def get_index():
    return index