from mistralai import Mistral
from dotenv import load_dotenv
import os

from agent.tools import search_tool, is_result_relevant
from agent.router import route, rephrase_query, get_query_type

load_dotenv()

# -----------------------------------------------
# Mistral Client
# -----------------------------------------------

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# -----------------------------------------------
# Main Agent Function
# -----------------------------------------------
# Ye poora agentic loop hai:
# 1. Query lo
# 2. Search karo
# 3. Router se pucho — answer do ya retry karo?
# 4. Retry pe query rephrase karo
# 5. Enough context mile to answer generate karo

def run_agent(query: str, bm25_retriever) -> str:
    
    print(f"\n{'='*50}")
    print(f"[Agent] New Query: {query}")
    print(f"{'='*50}")
    
    # Query type samjho
    query_type = get_query_type(query)
    print(f"[Agent] Query Type: {query_type}")
    
    all_results = []   # Sare retrieved chunks yahan store honge
    retry_count = 0    # Kitni baar retry hua
    current_query = query  # Current search query
    
    # -----------------------------------------------
    # AGENTIC LOOP — Yahi hai agentic RAG ka dil!
    # Jab tak router "answer" nahi kehta, loop chalta hai
    # -----------------------------------------------
    
    while True:
        
        print(f"\n[Agent] Loop iteration {retry_count + 1}")
        
        # -------------------------------------------
        # Step 1: Search Tool Call karo
        # -------------------------------------------
        tool_result = search_tool(
            query=current_query,
            bm25_retriever=bm25_retriever
        )
        
        # -------------------------------------------
        # Step 2: Results collect karo
        # -------------------------------------------
        if tool_result["success"]:
            new_results = tool_result["results"]
            all_results.extend(new_results)
            # Duplicates remove karo
            all_results = list(set(all_results))
            print(f"[Agent] Total chunks collected: {len(all_results)}")
        
        # -------------------------------------------
        # Step 3: Router se pucho — kya karna hai?
        # -------------------------------------------
        decision = route(
            query=current_query,
            results=all_results,
            retry_count=retry_count
        )
        
        # -------------------------------------------
        # Step 4: Router ka decision follow karo
        # -------------------------------------------
        
        if decision == "answer":
            # Enough context — answer generate karo
            break
        
        elif decision == "retry":
            # Query rephrase karo aur dobara search karo
            retry_count += 1
            current_query = rephrase_query(query, retry_count)
            print(f"[Agent] Rephrased query: {current_query}")
    
    # -----------------------------------------------
    # Step 5: Final Answer Generate karo Mistral se
    # -----------------------------------------------
    
    print(f"\n[Agent] Generating final answer...")
    
    context = "\n\n".join(all_results)
    
    prompt = f"""
You are a helpful AI assistant.
Answer ONLY from the provided context.
Be precise and detailed in your answer.

Context:
{context}

Question:
{query}

Answer:
"""
    
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.choices[0].message.content