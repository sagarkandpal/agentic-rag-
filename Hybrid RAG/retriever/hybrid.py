# retriever/hybrid.py

from retriever.vector_retriever import vector_search


def hybrid_search(query, bm25_retriever):

    # BM25 results
    bm25_docs = bm25_retriever.invoke(query)

    bm25_results = [
        doc.page_content for doc in bm25_docs
    ]

    # Pinecone results
    vector_results = vector_search(query)

    # Merge both
    combined_results = bm25_results + vector_results

    # Remove duplicates
    unique_results = list(set(combined_results))

    return unique_results