"""
Comprehensive Test Suite for Car Rental Chatbot System
Self-proposed test: Multi-dimensional evaluation of RAG system performance
"""

import time
import json
from datetime import datetime
import os

def run_comprehensive_evaluation():
    """
    Self-proposed test: Comprehensive evaluation of the RAG system
    Motivation: Evaluate the system across multiple dimensions including:
    1. Performance metrics (speed, accuracy)
    2. Quality of responses (relevance, completeness)
    3. System robustness (error handling, edge cases)
    4. User experience (response clarity, helpfulness)
    """
    
    print("=" * 80)
    print("COMPREHENSIVE RAG SYSTEM EVALUATION")
    print("=" * 80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {},
        'summary': {}
    }
    
    # Test 1: Performance Benchmarking
    print("TEST 1: PERFORMANCE BENCHMARKING")
    print("-" * 50)
    performance_results = run_performance_benchmark()
    results['tests']['performance'] = performance_results
    
    # Test 2: Quality Assessment
    print("\nTEST 2: RESPONSE QUALITY ASSESSMENT")
    print("-" * 50)
    quality_results = run_quality_assessment()
    results['tests']['quality'] = quality_results
    
    # Test 3: Edge Case Testing
    print("\nTEST 3: EDGE CASE TESTING")
    print("-" * 50)
    edge_case_results = run_edge_case_testing()
    results['tests']['edge_cases'] = edge_case_results
    
    # Test 4: Comparative Analysis
    print("\nTEST 4: COMPARATIVE ANALYSIS")
    print("-" * 50)
    comparative_results = run_comparative_analysis()
    results['tests']['comparative'] = comparative_results
    
    # Test 5: User Experience Evaluation
    print("\nTEST 5: USER EXPERIENCE EVALUATION")
    print("-" * 50)
    ux_results = run_ux_evaluation()
    results['tests']['user_experience'] = ux_results
    
    # Generate Summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE EVALUATION SUMMARY")
    print("=" * 80)
    
    summary = generate_evaluation_summary(results)
    results['summary'] = summary
    
    # Save results
    save_results(results)
    
    return results

def run_performance_benchmark():
    """Test system performance across different scenarios"""
    print("Running performance benchmark...")
    
    # Test different query complexities based on real rental data
    test_queries = {
        'simple': [
            "What types of engines are available for rental?",
            "How many rental units are available?",
            "What are the different rating levels for vehicles?"
        ],
        'complex': [
            "Which electric vehicles with high ratings have the best discount-to-units ratio?",
            "What is the optimal rental duration strategy for hybrid cars with medium ratings?",
            "How should we balance inventory between different engine types based on current availability?"
        ],
        'analytical': [
            "Analyze the relationship between rental duration (days) and discount percentages",
            "What patterns can you identify in discount distribution across different engine types?",
            "Provide recommendations for fleet optimization based on current rental data and availability"
        ]
    }
    
    results = {}
    
    try:
        from query_index import load_vector_index, test_query_performance
        
        for complexity, queries in test_queries.items():
            print(f"  Testing {complexity} queries...")
            start_time = time.time()
            
            # Load index
            index = load_vector_index("llama3.2")
            if index is None:
                results[complexity] = {'error': 'Failed to load index'}
                continue
            
            # Test queries
            query_results = []
            for query in queries:
                try:
                    from langchain_ollama import ChatOllama
                    chat_llama3 = ChatOllama(model="llama3.2", temperature=0.7)
                    
                    query_start = time.time()
                    answer = index.query(query, llm=chat_llama3)
                    query_time = time.time() - query_start
                    
                    query_results.append({
                        'query': query,
                        'answer': answer,
                        'time': query_time
                    })
                except Exception as e:
                    query_results.append({
                        'query': query,
                        'error': str(e),
                        'time': None
                    })
            
            total_time = time.time() - start_time
            avg_time = sum(r['time'] for r in query_results if r['time']) / len([r for r in query_results if r['time']])
            
            results[complexity] = {
                'total_time': total_time,
                'avg_query_time': avg_time,
                'successful_queries': len([r for r in query_results if r['time']]),
                'total_queries': len(queries),
                'queries': query_results
            }
            
            print(f"    {complexity}: {results[complexity]['successful_queries']}/{results[complexity]['total_queries']} successful, avg {avg_time:.2f}s")
    
    except Exception as e:
        results['error'] = str(e)
        print(f"  Performance benchmark failed: {e}")
    
    return results

def run_quality_assessment():
    """Assess the quality of responses"""
    print("Running quality assessment...")
    
    quality_queries = [
        {
            'query': "What types of engines are available for rental?",
            'expected_elements': ['Hybrid', 'Electric', 'Gasoline', 'Diesel'],
            'category': 'factual'
        },
        {
            'query': "Which vehicles have high ratings and how many units are available?",
            'expected_elements': ['High', 'rating', 'units', 'available'],
            'category': 'analytical'
        },
        {
            'query': "What are the different rental durations available?",
            'expected_elements': ['days', 'duration', '3', '4', '5', '6', '7', '8'],
            'category': 'statistical'
        },
        {
            'query': "What discount percentages are available for different engine types?",
            'expected_elements': ['discount', 'percentage', 'engine', 'type'],
            'category': 'pricing'
        },
        {
            'query': "How should we optimize our rental fleet based on current data?",
            'expected_elements': ['recommendation', 'optimization', 'fleet', 'strategy'],
            'category': 'advisory'
        }
    ]
    
    results = []
    
    try:
        from query_index import load_vector_index
        from langchain_ollama import ChatOllama
        
        index = load_vector_index("llama3.2")
        if index is None:
            return {'error': 'Failed to load index'}
        
        chat_llama3 = ChatOllama(model="llama3.2", temperature=0.7)
        
        for test_case in quality_queries:
            print(f"  Testing: {test_case['query']}")
            
            try:
                query_start = time.time()
                answer = index.query(test_case['query'], llm=chat_llama3)
                query_time = time.time() - query_start
                
                # Analyze answer quality
                answer_lower = answer.lower()
                elements_found = [elem for elem in test_case['expected_elements'] if elem.lower() in answer_lower]
                
                quality_score = len(elements_found) / len(test_case['expected_elements'])
                
                result = {
                    'query': test_case['query'],
                    'category': test_case['category'],
                    'answer': answer,
                    'time': query_time,
                    'expected_elements': test_case['expected_elements'],
                    'elements_found': elements_found,
                    'quality_score': quality_score,
                    'answer_length': len(answer)
                }
                
                results.append(result)
                print(f"    Quality score: {quality_score:.2f} ({len(elements_found)}/{len(test_case['expected_elements'])} elements found)")
                
            except Exception as e:
                results.append({
                    'query': test_case['query'],
                    'error': str(e),
                    'quality_score': 0
                })
                print(f"    Error: {e}")
    
    except Exception as e:
        return {'error': str(e)}
    
    return results

def run_edge_case_testing():
    """Test system behavior with edge cases"""
    print("Running edge case testing...")
    
    edge_cases = [
        "What is the meaning of life?",
        "How do I cook pasta?",
        "Show me all vehicles with rating 'SuperDuperHigh'",
        "What cars are available for negative rental days?",
        "Give me the exact GPS coordinates of all rental vehicles",
        "What is the square root of the average discount percentage?",
        "Show me vehicles with infinite rental units available",
        "What is the color of the rental vehicles?",
        "How many vehicles have a rating of 'Purple' or 'Gold'?",
        "What is the weather forecast for rental days?",
        "Show me vehicles with discount percentages over 100%",
        "What cars are available for 0 days rental?",
        "How many vehicles have negative units available?",
        "What is the fuel efficiency of the rental vehicles?",
        "Show me vehicles with rating 'Excellent' or 'Perfect'"
    ]
    
    results = []
    
    try:
        from query_index import load_vector_index
        from langchain_ollama import ChatOllama
        
        index = load_vector_index("llama3.2")
        if index is None:
            return {'error': 'Failed to load index'}
        
        chat_llama3 = ChatOllama(model="llama3.2", temperature=0.7)
        
        for i, query in enumerate(edge_cases, 1):
            print(f"  Edge case {i}: {query[:50]}...")
            
            try:
                query_start = time.time()
                answer = index.query(query, llm=chat_llama3)
                query_time = time.time() - query_start
                
                # Analyze response appropriateness
                answer_lower = answer.lower()
                inappropriate_responses = ['i don\'t know', 'not available', 'no data', 'error']
                is_appropriate = not any(phrase in answer_lower for phrase in inappropriate_responses)
                
                result = {
                    'query': query,
                    'answer': answer,
                    'time': query_time,
                    'is_appropriate': is_appropriate,
                    'answer_length': len(answer)
                }
                
                results.append(result)
                print(f"    Appropriate: {is_appropriate}, Length: {len(answer)} chars")
                
            except Exception as e:
                results.append({
                    'query': query,
                    'error': str(e),
                    'is_appropriate': False
                })
                print(f"    Error: {e}")
    
    except Exception as e:
        return {'error': str(e)}
    
    return results

def run_comparative_analysis():
    """Compare different system configurations"""
    print("Running comparative analysis...")
    
    configurations = [
        {'name': 'CSV_RAG', 'type': 'csv', 'model': 'llama3.2'},
        {'name': 'PDF_RAG', 'type': 'pdf', 'model': 'llama3.2'},
        {'name': 'Non_RAG', 'type': 'non_rag', 'model': 'llama3.2'}
    ]
    
    test_queries = [
        "What types of engines are available for rental?",
        "Which vehicles have high ratings and how many units are available?",
        "What are the different rental durations available and their discount rates?"
    ]
    
    results = {}
    
    for config in configurations:
        print(f"  Testing {config['name']}...")
        
        try:
            if config['type'] == 'csv':
                from query_index import load_vector_index
                from langchain_ollama import ChatOllama
                
                index = load_vector_index(config['model'])
                if index is None:
                    results[config['name']] = {'error': 'Failed to load index'}
                    continue
                
                chat_llama3 = ChatOllama(model=config['model'], temperature=0.7)
                
                config_results = []
                for query in test_queries:
                    query_start = time.time()
                    answer = index.query(query, llm=chat_llama3)
                    query_time = time.time() - query_start
                    
                    config_results.append({
                        'query': query,
                        'answer': answer,
                        'time': query_time
                    })
                
            elif config['type'] == 'pdf':
                from query_index_pdf import load_vector_index_pdf
                from langchain_ollama import ChatOllama
                
                index = load_vector_index_pdf(config['model'])
                if index is None:
                    results[config['name']] = {'error': 'Failed to load PDF index'}
                    continue
                
                chat_llama3 = ChatOllama(model=config['model'], temperature=0.7)
                
                config_results = []
                for query in test_queries:
                    query_start = time.time()
                    answer = index.query(query, llm=chat_llama3)
                    query_time = time.time() - query_start
                    
                    config_results.append({
                        'query': query,
                        'answer': answer,
                        'time': query_time
                    })
                
            elif config['type'] == 'non_rag':
                from langchain_ollama import ChatOllama
                
                chat_llama3 = ChatOllama(model=config['model'], temperature=0.7)
                
                config_results = []
                for query in test_queries:
                    query_start = time.time()
                    answer = chat_llama3.invoke(query)
                    query_time = time.time() - query_start
                    
                    config_results.append({
                        'query': query,
                        'answer': answer.content,
                        'time': query_time
                    })
            
            # Calculate metrics
            avg_time = sum(r['time'] for r in config_results) / len(config_results)
            avg_length = sum(len(r['answer']) for r in config_results) / len(config_results)
            
            results[config['name']] = {
                'avg_time': avg_time,
                'avg_answer_length': avg_length,
                'queries': config_results
            }
            
            print(f"    Avg time: {avg_time:.2f}s, Avg length: {avg_length:.0f} chars")
            
        except Exception as e:
            results[config['name']] = {'error': str(e)}
            print(f"    Error: {e}")
    
    return results

def run_ux_evaluation():
    """Evaluate user experience aspects"""
    print("Running UX evaluation...")
    
    ux_queries = [
        "Help me find a good rental car for a weekend trip (3-4 days)",
        "I need a rental car for business travel, what do you recommend?",
        "What's the best rental deal available right now with high discounts?",
        "I'm environmentally conscious, what electric or hybrid rental options do you have?",
        "I need a rental car for 5 days, what vehicles are available and what discounts apply?",
        "I want a high-rated vehicle with good discount, what are my options?",
        "What rental vehicles have the most units available for immediate booking?",
        "I'm looking for a long-term rental (7-8 days), what discounts are available?"
    ]
    
    results = []
    
    try:
        from query_index import load_vector_index
        from langchain_ollama import ChatOllama
        
        index = load_vector_index("llama3.2")
        if index is None:
            return {'error': 'Failed to load index'}
        
        chat_llama3 = ChatOllama(model="llama3.2", temperature=0.7)
        
        for query in ux_queries:
            print(f"  UX Test: {query}")
            
            try:
                query_start = time.time()
                answer = index.query(query, llm=chat_llama3)
                query_time = time.time() - query_start
                
                # Evaluate UX aspects
                answer_lower = answer.lower()
                is_helpful = any(word in answer_lower for word in ['recommend', 'suggest', 'available', 'option', 'good', 'best'])
                is_personalized = any(word in answer_lower for word in ['you', 'your', 'based on', 'for you'])
                is_actionable = any(word in answer_lower for word in ['can', 'should', 'try', 'consider', 'choose'])
                
                ux_score = sum([is_helpful, is_personalized, is_actionable]) / 3
                
                result = {
                    'query': query,
                    'answer': answer,
                    'time': query_time,
                    'is_helpful': is_helpful,
                    'is_personalized': is_personalized,
                    'is_actionable': is_actionable,
                    'ux_score': ux_score
                }
                
                results.append(result)
                print(f"    UX Score: {ux_score:.2f} (Helpful: {is_helpful}, Personalized: {is_personalized}, Actionable: {is_actionable})")
                
            except Exception as e:
                results.append({
                    'query': query,
                    'error': str(e),
                    'ux_score': 0
                })
                print(f"    Error: {e}")
    
    except Exception as e:
        return {'error': str(e)}
    
    return results

def generate_evaluation_summary(results):
    """Generate a comprehensive summary of all test results"""
    summary = {
        'overall_score': 0,
        'performance_score': 0,
        'quality_score': 0,
        'robustness_score': 0,
        'ux_score': 0,
        'recommendations': []
    }
    
    # Performance summary
    if 'performance' in results['tests'] and 'error' not in results['tests']['performance']:
        perf = results['tests']['performance']
        total_queries = sum(config['total_queries'] for config in perf.values() if isinstance(config, dict) and 'total_queries' in config)
        successful_queries = sum(config['successful_queries'] for config in perf.values() if isinstance(config, dict) and 'successful_queries' in config)
        summary['performance_score'] = (successful_queries / total_queries) * 100 if total_queries > 0 else 0
    
    # Quality summary
    if 'quality' in results['tests'] and isinstance(results['tests']['quality'], list):
        quality_scores = [r['quality_score'] for r in results['tests']['quality'] if 'quality_score' in r]
        summary['quality_score'] = sum(quality_scores) / len(quality_scores) * 100 if quality_scores else 0
    
    # Robustness summary
    if 'edge_cases' in results['tests'] and isinstance(results['tests']['edge_cases'], list):
        appropriate_responses = [r['is_appropriate'] for r in results['tests']['edge_cases'] if 'is_appropriate' in r]
        summary['robustness_score'] = sum(appropriate_responses) / len(appropriate_responses) * 100 if appropriate_responses else 0
    
    # UX summary
    if 'user_experience' in results['tests'] and isinstance(results['tests']['user_experience'], list):
        ux_scores = [r['ux_score'] for r in results['tests']['user_experience'] if 'ux_score' in r]
        summary['ux_score'] = sum(ux_scores) / len(ux_scores) * 100 if ux_scores else 0
    
    # Overall score
    scores = [summary['performance_score'], summary['quality_score'], summary['robustness_score'], summary['ux_score']]
    summary['overall_score'] = sum(scores) / len(scores)
    
    # Generate recommendations
    if summary['performance_score'] < 80:
        summary['recommendations'].append("Improve system performance - consider optimizing indexing or query processing")
    if summary['quality_score'] < 80:
        summary['recommendations'].append("Enhance response quality - improve prompt engineering or data enrichment")
    if summary['robustness_score'] < 80:
        summary['recommendations'].append("Strengthen error handling and edge case management")
    if summary['ux_score'] < 80:
        summary['recommendations'].append("Improve user experience - make responses more helpful and actionable")
    
    return summary

def save_results(results):
    """Save test results to file"""
    os.makedirs("test_results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results/comprehensive_evaluation_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {filename}")

if __name__ == "__main__":
    run_comprehensive_evaluation()
