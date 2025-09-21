from langchain_ollama import ChatOllama
import pickle
import os
import time

def load_vector_index_pdf(model_name="llama3.2"):
    """Load the saved PDF vector index with timing measurements"""
    index_file = f"saved_index/vector_index_{model_name.replace('.', '_')}_rentals_pdf.pkl"
    
    if not os.path.exists(index_file):
        print(f"Error: PDF Vector index not found for model {model_name}. Please run create_index_pdf.py first.")
        return None
    
    start_time = time.time()
    with open(index_file, "rb") as f:
        index = pickle.load(f)
    load_time = time.time() - start_time
    
    print(f"PDF Vector index loaded successfully in {load_time:.2f} seconds!")
    return index

def query_chatbot_pdf(model_name="llama3.2"):
    """Interactive chatbot for querying the PDF vector index with timing measurements"""
    
    # Load the vector index
    index = load_vector_index_pdf(model_name)
    if index is None:
        return
    
    # Create a ChatOllama object
    chat_llama3 = ChatOllama(model=model_name, temperature=0.7)
    
    print(f"PDF Chatbot ready with model {model_name}! Type 'exit' to quit.")
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
            
            print(f"PDF Chatbot: {answer}")
            print(f"Query processed in {query_time:.2f} seconds")
            print("-" * 40)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 40)

def test_query_performance_pdf(model_name="llama3.2", test_queries=None):
    """Test PDF query performance with predefined queries"""
    if test_queries is None:
        test_queries = [
            "What types of engines are available in our fleet?",
            "Which vehicles have high customer ratings?",
            "What are the most popular rental durations?",
            "Show me electric vehicles with available discounts",
            "How many hybrid cars are currently available?",
            "What is the average discount rate across all vehicles?",
            "Which engine type has the most units available?",
            "What business insights can you provide about our fleet?",
            "How should we optimize our pricing strategy?",
            "What are the key recommendations for inventory management?"
        ]
    
    print(f"Testing PDF query performance with model: {model_name}")
    print("=" * 60)
    
    # Load the vector index
    index = load_vector_index_pdf(model_name)
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
    print("PDF QUERY PERFORMANCE SUMMARY")
    print("=" * 60)
    total_time = sum(r['time'] for r in results if r['time'])
    avg_time = total_time / len([r for r in results if r['time']])
    
    print(f"Total queries: {len(results)}")
    print(f"Successful queries: {len([r for r in results if r['time']])}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per query: {avg_time:.2f} seconds")
    
    return results

def compare_csv_vs_pdf():
    """Compare query performance between CSV and PDF versions"""
    print("COMPARING CSV vs PDF QUERY PERFORMANCE")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "What types of engines are available?",
        "Which cars have high ratings?",
        "Show me electric cars with discounts"
    ]
    
    # Test CSV version
    print("\nTesting CSV version...")
    print("-" * 40)
    try:
        from query_index import test_query_performance
        csv_results = test_query_performance("llama3.2", test_queries)
        csv_avg = sum(r['time'] for r in csv_results if r['time']) / len([r for r in csv_results if r['time']])
    except Exception as e:
        print(f"CSV test failed: {e}")
        csv_results = None
        csv_avg = None
    
    # Test PDF version
    print("\nTesting PDF version...")
    print("-" * 40)
    try:
        pdf_results = test_query_performance_pdf("llama3.2", test_queries)
        pdf_avg = sum(r['time'] for r in pdf_results if r['time']) / len([r for r in pdf_results if r['time']])
    except Exception as e:
        print(f"PDF test failed: {e}")
        pdf_results = None
        pdf_avg = None
    
    # Comparison
    print("\n" + "=" * 60)
    print("CSV vs PDF COMPARISON SUMMARY")
    print("=" * 60)
    
    if csv_avg and pdf_avg:
        print(f"CSV average query time: {csv_avg:.2f} seconds")
        print(f"PDF average query time: {pdf_avg:.2f} seconds")
        if pdf_avg > csv_avg:
            print(f"PDF is {((pdf_avg - csv_avg) / csv_avg * 100):.1f}% slower than CSV")
        else:
            print(f"PDF is {((csv_avg - pdf_avg) / pdf_avg * 100):.1f}% faster than CSV")
    
    return csv_results, pdf_results

if __name__ == "__main__":
    # Run interactive PDF chatbot
    query_chatbot_pdf()
    
    # Uncomment to run performance tests
    # test_query_performance_pdf()
    # compare_csv_vs_pdf()
