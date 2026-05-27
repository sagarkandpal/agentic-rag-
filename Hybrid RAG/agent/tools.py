from retriever.hybrid import hybrid_search

# -----------------------------------------------
# Tool 1: Hybrid Search
# -----------------------------------------------
# Ye tool agent call karta hai jab use
# PDF se kuch retrieve karna hota hai.
# Tera existing hybrid_search as it is use ho raha hai!

def search_tool(query: str, bm25_retriever) -> dict:
    
    print(f"\n[Tool] Searching for: {query}")
    
    results = hybrid_search(
        query=query,
        bm25_retriever=bm25_retriever
    )
    
    if not results:
        return {
            "success": False,
            "results": [],
            "message": "Kuch nahi mila is query se"
        }
    
    return {
        "success": True,
        "results": results,
        "message": f"{len(results)} chunks mile"
    }


# -----------------------------------------------
# Tool 2: Result Quality Check
# -----------------------------------------------
# Agent check karta hai ki jo results aaye
# wo query ke liye relevant hain ya nahi.
# Simple length + keyword check se decide karta hai.

def is_result_relevant(query: str, results: list) -> bool:
    
    if not results:
        return False
    
    # Agar results mein query ke words hain to relevant hai
    query_words = set(query.lower().split())
    
    for result in results:
        result_words = set(result.lower().split())
        # Agar 30% words match ho to relevant maano
        overlap = query_words.intersection(result_words)
        if len(overlap) / len(query_words) > 0.3:
            return True
    
    return False