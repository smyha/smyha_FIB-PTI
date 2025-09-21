"""
Master script to run all tests and generate comprehensive report
"""

import subprocess
import sys, os
import time
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and capture output"""
    print(f"\n{'='*80}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Duration: {duration:.2f} seconds")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("\nSTDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        return {
            'script': script_name,
            'description': description,
            'duration': duration,
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
        
    except subprocess.TimeoutExpired:
        print(f"Script {script_name} timed out after 300 seconds")
        return {
            'script': script_name,
            'description': description,
            'duration': 300,
            'return_code': -1,
            'stdout': '',
            'stderr': 'Timeout after 300 seconds',
            'success': False
        }
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return {
            'script': script_name,
            'description': description,
            'duration': 0,
            'return_code': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }

def main():
    """Run all tests and generate report"""
    print("CAR RENTAL CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define test sequence
    tests = [
        ("convert_csv_to_pdf.py", "Convert CSV to enriched PDF"),
        ("real_data_demo.py", "Run demo with real rental data from JSON"),
        ("mock_demo_enhanced.py", "Run enhanced mock demo with realistic rental data"),
        ("create_index.py", "Create vector index from CSV (with timing)"),
        ("create_index_pdf.py", "Create vector index from PDF (with timing)"),
        ("query_index.py", "Test CSV-based RAG queries"),
        ("query_index_pdf.py", "Test PDF-based RAG queries"),
        ("query_non_rag.py", "Test non-RAG queries"),
        ("comprehensive_test.py", "Run comprehensive evaluation suite")
    ]
    
    results = []
    
    for script, description in tests:
        result = run_script(script, description)
        results.append(result)
        
        # Add delay between tests
        time.sleep(2)
    
    # Generate summary report
    print(f"\n{'='*80}")
    print("TEST EXECUTION SUMMARY")
    print(f"{'='*80}")
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    total_tests = len(results)
    successful_count = len(successful_tests)
    failed_count = len(failed_tests)
    success_rate = successful_count/total_tests*100
    
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {failed_count}")
    print(f"Success rate: {success_rate:.1f}%")
    
    if successful_tests:
        print("\nSuccessful tests:")
        for result in successful_tests:
            print(f"  ✓ {result['description']} ({result['duration']:.2f}s)")
    
    if failed_tests:
        print("\nFailed tests:")
        for result in failed_tests:
            print(f"  ✗ {result['description']} (Error: {result['stderr'][:100]}...)")
    
    # Performance summary
    total_duration = sum(r['duration'] for r in results)
    print(f"\nTotal execution time: {total_duration:.2f} seconds")
    
    # Save detailed results
    import json
    os.makedirs("test_results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results/test_execution_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(results),
                'successful_tests': len(successful_tests),
                'failed_tests': len(failed_tests),
                'success_rate': len(successful_tests)/len(results)*100,
                'total_duration': total_duration
            },
            'results': results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")
    
    print(f"\n{'='*80}")
    print("TEST EXECUTION COMPLETED")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
