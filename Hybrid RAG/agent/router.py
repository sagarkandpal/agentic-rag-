# -----------------------------------------------
# Router — Query ka type decide karta hai
# -----------------------------------------------
# Agent router se puchta hai:
# "Is query ke liye kya karna chahiye?"
# Router decide karta hai — search, retry, ya answer do

# Query Types:
# "search"  → Normal hybrid search karo
# "retry"   → Query rephrase karke dobara search karo
# "answer"  → Enough context hai, answer generate karo
# "unknown" → Kuch samajh nahi aaya

# Keywords jo query type decide karte hain
TIMELINE_KEYWORDS = [
    "when", "year", "date", "kab", "konse saal",
    "timeline", "history", "born", "died"
]

COMPARISON_KEYWORDS = [
    "compare", "difference", "vs", "better",
    "tulna", "fark", "versus"
]

SIMPLE_KEYWORDS = [
    "what", "who", "kya", "kaun", "batao",
    "tell", "explain", "describe"
]


def get_query_type(query: str) -> str:
    
    query_lower = query.lower()
    
    # Timeline/date based query
    if any(word in query_lower for word in TIMELINE_KEYWORDS):
        return "timeline"
    
    # Comparison query — multiple searches lagegi
    if any(word in query_lower for word in COMPARISON_KEYWORDS):
        return "comparison"
    
    # Simple factual query
    if any(word in query_lower for word in SIMPLE_KEYWORDS):
        return "simple"
    
    return "simple"  # Default


def route(query: str, results: list, retry_count: int) -> str:
    
    # -----------------------------------------------
    # Rule 1: Agar 2 baar retry ho chuka to bas karo
    # -----------------------------------------------
    if retry_count >= 2:
        print("[Router] Max retries reached — answering with what we have")
        return "answer"
    
    # -----------------------------------------------
    # Rule 2: Agar results hi nahi aaye to retry karo
    # -----------------------------------------------
    if not results:
        print("[Router] No results — retrying")
        return "retry"
    
    # -----------------------------------------------
    # Rule 3: Agar sirf 1 result aaya to retry karo
    # -----------------------------------------------
    if len(results) < 2:
        print("[Router] Very few results — retrying")
        return "retry"
    
    # -----------------------------------------------
    # Rule 4: Results theek hain — answer generate karo
    # -----------------------------------------------
    print(f"[Router] {len(results)} results found — generating answer")
    return "answer"


def rephrase_query(query: str, retry_count: int) -> str:
    
    # -----------------------------------------------
    # Retry pe query ko thoda modify karo
    # taaki different results aayein
    # -----------------------------------------------
    
    if retry_count == 1:
        return f"Tell me about {query}"
    
    if retry_count == 2:
        return f"Information regarding {query} in detail"
    
    return query