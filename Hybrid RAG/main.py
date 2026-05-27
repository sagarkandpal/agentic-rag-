from dotenv import load_dotenv
import os

from mistralai import Mistral

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingest.upsert import upsert_documents
from retriever.bm25_retriever import create_bm25_retriever
from retriever.hybrid import hybrid_search

from agent.agent import run_agent

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Initialize Mistral Client
# ---------------------------------------------------

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# ---------------------------------------------------
# Load PDF
# ---------------------------------------------------

loader = PyPDFLoader("data/cr7biography.pdf")

documents = loader.load()

print(f"\nLoaded {len(documents)} pages from PDF")

# ---------------------------------------------------
# Split Documents into Chunks
# ---------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

split_docs = text_splitter.split_documents(documents)

# Extract text chunks
chunks = [doc.page_content for doc in split_docs]

print(f"Created {len(chunks)} chunks")

# ---------------------------------------------------
# Upload Chunks to Pinecone
# ---------------------------------------------------

# ----------------------------------------
# Sirf pehli baar upsert karo
# ----------------------------------------
already_upserted = os.path.exists("data/.upserted")

if not already_upserted:
    print("First time — Uploading chunks to Pinecone...")
    upsert_documents(chunks)
    # Flag file bana do
    open("data/.upserted", "w").close()
    print("Upload done!")
else:
    print("Chunks already in Pinecone — Skipping upsert! ✅")

# ---------------------------------------------------
# Create BM25 Retriever
# ---------------------------------------------------

bm25_retriever = create_bm25_retriever(chunks)

# ---------------------------------------------------
# Conversation Loop
# ---------------------------------------------------

print("\nAgentic RAG Chat started! Type 'exit' to stop.\n")

while True:
    
    query = input("You: ").strip()
    
    if query.lower() in ["exit", "quit", "over", "0"]:
        print("Goodbye!")
        break
    
    if not query:
        continue
    
    # Agent ko call karo — wo khud decide karega
    answer = run_agent(
        query=query,
        bm25_retriever=bm25_retriever
    )
    
    print(f"\nBot: {answer}\n")