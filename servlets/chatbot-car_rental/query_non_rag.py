from langchain_ollama import ChatOllama
import time

def query_chatbot_non_rag(model_name="llama3.2"):
    """Interactive chatbot without RAG (no vector index) with timing measurements"""
    
    # Create a ChatOllama object
    chat_llama3 = ChatOllama(model=model_name, temperature=0.7)
    
    print(f"Non-RAG Chatbot ready with model {model_name}! Type 'exit' to quit.")
    print("Note: This chatbot has no access to the rental data - it will answer based on its training data only.")
    print("-" * 40)
    
    prompt = ""
    while prompt.lower() != "exit":
        # Use ChatOllama object to answer questions
        prompt = input("Enter your query: ")
        
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
            
        try:
            query_start = time.time()
            # Direct query without RAG context
            answer = chat_llama3.invoke(prompt)
            query_time = time.time() - query_start
            
            print(f"Non-RAG Chatbot: {answer.content}")
            print(f"Query processed in {query_time:.2f} seconds")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 40)

def test_query_performance_non_rag(model_name="llama3.2", test_queries=None):
    """Test non-RAG query performance with predefined queries"""
    if test_queries is None:
        test_queries = [
            "What types of engines are available in car rentals?",
            "Which cars typically have high ratings?",
            "What are common rental durations?",
            "Show me information about electric cars with discounts",
            "How many hybrid cars are usually available?",
            "What is the average discount rate for car rentals?",
            "Which engine type is most popular for rentals?",
            "What business insights can you provide about car rental fleets?",
            "How should car rental companies optimize pricing?",
            "What are key recommendations for rental inventory management?"
        ]
    
    print(f"Testing non-RAG query performance with model: {model_name}")
    print("=" * 60)
    
    # Create a ChatOllama object
    chat_llama3 = ChatOllama(model=model_name, temperature=0.7)
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 40)
        
        try:
            query_start = time.time()
            answer = chat_llama3.invoke(query)
            query_time = time.time() - query_start
            
            print(f"Answer: {answer.content}")
            print(f"Time: {query_time:.2f} seconds")
            
            results.append({
                'query': query,
                'answer': answer.content,
                'time': query_time
            })
            
        except Exception as e:
            print(f"Error: {e}")
            results.append({
                'query': query,
                'answer': f"Error: {e}",
                'time': None
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("NON-RAG QUERY PERFORMANCE SUMMARY")
    print("=" * 60)
    total_time = sum(r['time'] for r in results if r['time'])
    avg_time = total_time / len([r for r in results if r['time']])
    
    print(f"Total queries: {len(results)}")
    print(f"Successful queries: {len([r for r in results if r['time']])}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per query: {avg_time:.2f} seconds")
    
    return results

def compare_rag_vs_non_rag():
    """Compare RAG vs non-RAG query performance and quality"""
    print("COMPARING RAG vs NON-RAG PERFORMANCE")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "What types of engines are available?",
        "Which cars have high ratings?",
        "Show me electric cars with discounts",
        "How many hybrid cars are available?",
        "What is the average discount rate?"
    ]
    
    # Test RAG version (CSV)
    print("\nTesting RAG version (CSV)...")
    print("-" * 40)
    try:
        from query_index import test_query_performance
        rag_results = test_query_performance("llama3.2", test_queries)
        rag_avg = sum(r['time'] for r in rag_results if r['time']) / len([r for r in rag_results if r['time']])
    except Exception as e:
        print(f"RAG test failed: {e}")
        rag_results = None
        rag_avg = None
    
    # Test non-RAG version
    print("\nTesting non-RAG version...")
    print("-" * 40)
    try:
        non_rag_results = test_query_performance_non_rag("llama3.2", test_queries)
        non_rag_avg = sum(r['time'] for r in non_rag_results if r['time']) / len([r for r in non_rag_results if r['time']])
    except Exception as e:
        print(f"Non-RAG test failed: {e}")
        non_rag_results = None
        non_rag_avg = None
    
    # Comparison
    print("\n" + "=" * 60)
    print("RAG vs NON-RAG COMPARISON SUMMARY")
    print("=" * 60)
    
    if rag_avg and non_rag_avg:
        print(f"RAG average query time: {rag_avg:.2f} seconds")
        print(f"Non-RAG average query time: {non_rag_avg:.2f} seconds")
        if non_rag_avg > rag_avg:
            print(f"Non-RAG is {((non_rag_avg - rag_avg) / rag_avg * 100):.1f}% slower than RAG")
        else:
            print(f"Non-RAG is {((rag_avg - non_rag_avg) / non_rag_avg * 100):.1f}% faster than RAG")
    
    # Quality comparison
    print("\n" + "=" * 60)
    print("ANSWER QUALITY COMPARISON")
    print("=" * 60)
    
    if rag_results and non_rag_results:
        for i, (rag, non_rag) in enumerate(zip(rag_results, non_rag_results), 1):
            print(f"\nQuery {i}: {rag['query']}")
            print("-" * 40)
            print(f"RAG Answer: {rag['answer'][:200]}...")
            print(f"Non-RAG Answer: {non_rag['answer'][:200]}...")
            print(f"RAG Time: {rag['time']:.2f}s, Non-RAG Time: {non_rag['time']:.2f}s")
    
    return rag_results, non_rag_results

if __name__ == "__main__":
    # Run interactive non-RAG chatbot
    query_chatbot_non_rag()
    
    # Uncomment to run performance tests
    # test_query_performance_non_rag()
    # compare_rag_vs_non_rag()
