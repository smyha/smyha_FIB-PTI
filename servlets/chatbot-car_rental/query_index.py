from langchain_ollama import ChatOllama
import pickle
import os
import time

# Constants
DEFAULT_MODEL = "llama3.2"

def load_vector_index(model_name=DEFAULT_MODEL):
    """Load the saved vector index with timing measurements"""
    index_file = f"saved_index/vector_index_{model_name.replace('.', '_')}_rentals.pkl"
    
    if not os.path.exists(index_file):
        print(f"Error: Vector index not found for model {model_name}. Please run create_index.py first.")
        return None
    
    start_time = time.time()
    with open(index_file, "rb") as f:
        index = pickle.load(f)
    load_time = time.time() - start_time
    
    print(f"Vector index loaded successfully in {load_time:.2f} seconds!")
    return index

def query_chatbot(model_name=DEFAULT_MODEL):
    """Interactive chatbot for querying the vector index with timing measurements"""
    
    # Load the vector index
    index = load_vector_index(model_name)
    if index is None:
        return
    
    # Create a ChatOllama object
    chat_llama3 = ChatOllama(model=model_name, temperature=0.7)
    
    print(f"Chatbot ready with model {model_name}! Type 'exit' to quit.")
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
            answer = index.query(prompt, llm=chat_llama3)
            query_time = time.time() - query_start
            
            print(f"Llama3 Chatbot: {answer}")
            print(f"Query processed in {query_time:.2f} seconds")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 40)

def test_query_performance(model_name=DEFAULT_MODEL, test_queries=None):
    """Test query performance with predefined queries"""
    if test_queries is None:
        test_queries = [
            "What types of engines are available?",
            "Which cars have high ratings?",
            "What are the most expensive rentals?",
            "Show me electric cars with discounts",
            "How many units are available for hybrid cars?"
        ]
    
    print(f"Testing query performance with model: {model_name}")
    print("=" * 60)
    
    # Load the vector index
    index = load_vector_index(model_name)
    if index is None:
        return
    
    # Create a ChatOllama object
    chat_llama3 = ChatOllama(model=model_name, temperature=0.7)
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 40)
        
        try:
            query_start = time.time()
            answer = index.query(query, llm=chat_llama3)
            query_time = time.time() - query_start
            
            print(f"Answer: {answer}")
            print(f"Time: {query_time:.2f} seconds")
            
            results.append({
                'query': query,
                'answer': answer,
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
    print("QUERY PERFORMANCE SUMMARY")
    print("=" * 60)
    total_time = sum(r['time'] for r in results if r['time'])
    avg_time = total_time / len([r for r in results if r['time']])
    
    print(f"Total queries: {len(results)}")
    print(f"Successful queries: {len([r for r in results if r['time']])}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per query: {avg_time:.2f} seconds")
    
    return results

def compare_models():
    """Compare different models for query performance"""
    models = [DEFAULT_MODEL, "llama3.1"]
    test_queries = [
        "What types of engines are available?",
        "Which cars have high ratings?",
        "Show me electric cars with discounts"
    ]
    
    print("COMPARING MODELS FOR QUERY PERFORMANCE")
    print("=" * 60)
    
    all_results = {}
    
    for model in models:
        print(f"\nTesting model: {model}")
        print("-" * 40)
        results = test_query_performance(model, test_queries)
        all_results[model] = results
    
    # Compare results
    print("\n" + "=" * 60)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 60)
    
    for model, results in all_results.items():
        successful = [r for r in results if r['time']]
        if successful:
            avg_time = sum(r['time'] for r in successful) / len(successful)
            print(f"{model:15}: {len(successful)}/{len(results)} successful, avg {avg_time:.2f}s")
        else:
            print(f"{model:15}: No successful queries")

if __name__ == "__main__":
    # Run interactive chatbot
    query_chatbot()
    
    # Uncomment to run performance tests
    # test_query_performance()
    # compare_models()