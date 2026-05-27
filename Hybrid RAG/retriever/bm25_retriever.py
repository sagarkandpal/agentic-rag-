from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


def create_bm25_retriever(chunks):

    # Convert text chunks into Documents
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Create BM25 Retriever
    retriever = BM25Retriever.from_documents(docs)

    # Number of docs to return
    retriever.k = 3

    return retriever