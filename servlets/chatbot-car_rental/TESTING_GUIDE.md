# Car Rental Chatbot - Testing Guide

This guide explains how to run the comprehensive test suite for the car rental chatbot system.

## Overview

The test suite evaluates the RAG (Retrieval-Augmented Generation) system across multiple dimensions:

1. **Performance Testing** - Measure indexing and query response times
2. **Quality Assessment** - Evaluate answer accuracy and relevance
3. **Edge Case Testing** - Test system robustness with unusual queries
4. **Comparative Analysis** - Compare different system configurations
5. **User Experience Evaluation** - Assess response helpfulness and clarity

## Prerequisites

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running with the required models:
```bash
ollama pull llama3.2
ollama pull llama3.1
ollama pull nomic-embed-text
```

## Test Files

### Core Test Scripts

- `create_index.py` - Creates vector index from CSV with timing measurements
- `query_index.py` - Tests CSV-based RAG queries with performance metrics
- `create_index_pdf.py` - Creates vector index from enriched PDF
- `query_index_pdf.py` - Tests PDF-based RAG queries
- `query_non_rag.py` - Tests non-RAG queries for comparison
- `comprehensive_test.py` - Self-proposed comprehensive evaluation suite

### Utility Scripts

- `convert_csv_to_pdf.py` - Converts CSV data to enriched PDF format
- `run_all_tests.py` - Master script to run all tests sequentially

## Running Tests

### Option 1: Run All Tests (Recommended)

```bash
python run_all_tests.py
```

This will execute all tests in sequence and generate a comprehensive report.

### Option 2: Run Individual Tests

#### 4.1 Duration Measurement
```bash
# Test indexing performance
python create_index.py

# Test query performance
python query_index.py
```

#### 4.2 Answer Quality Comparison
```bash
# Test different models
python create_index.py  # Uncomment test_multiple_models() in the script
python query_index.py   # Uncomment compare_models() in the script
```

#### 4.3 PDF Dataset Testing
```bash
# Convert CSV to PDF
python convert_csv_to_pdf.py

# Create PDF index
python create_index_pdf.py

# Test PDF queries
python query_index_pdf.py
```

#### 4.4 RAG vs Non-RAG Comparison
```bash
# Test non-RAG version
python query_non_rag.py

# Compare RAG vs non-RAG
python query_index.py    # Uncomment compare_rag_vs_non_rag()
python query_non_rag.py  # Uncomment compare_rag_vs_non_rag()
```

#### 4.5 Self-Proposed Comprehensive Test
```bash
python comprehensive_test.py
```

## Test Results

### Output Files

- `test_results/` - Directory containing detailed test results
- `saved_index/` - Directory containing vector indices
- `dataset/rentals.pdf` - Enriched PDF version of the dataset

### Understanding Results

#### Performance Metrics
- **Indexing Time**: Time to create vector index from data
- **Query Time**: Time to process individual queries
- **Load Time**: Time to load pre-built indices

#### Quality Metrics
- **Quality Score**: Based on presence of expected elements in answers
- **Relevance**: How well answers match query intent
- **Completeness**: Whether answers cover all aspects of the query

#### Robustness Metrics
- **Edge Case Handling**: How well system handles unusual queries
- **Error Rate**: Percentage of failed queries
- **Appropriate Responses**: Whether responses are contextually appropriate

#### User Experience Metrics
- **Helpfulness**: Whether responses provide useful information
- **Personalization**: Whether responses feel tailored to the user
- **Actionability**: Whether responses suggest concrete next steps

## Expected Outcomes

### Performance Expectations
- CSV indexing: 2-10 seconds
- PDF indexing: 5-15 seconds
- Query response: 1-5 seconds per query

### Quality Expectations
- Quality score: >80% for factual queries
- Relevance: >70% for analytical queries
- Completeness: >60% for complex queries

### Comparative Results
- RAG should provide more accurate, data-specific answers
- PDF version should offer richer context and insights
- Non-RAG should be faster but less accurate for specific data

## Troubleshooting

### Common Issues

1. **Ollama not running**
   - Start Ollama service: `ollama serve`
   - Pull required models: `ollama pull llama3.2`

2. **Missing dependencies**
   - Install requirements: `pip install -r requirements.txt`

3. **Index not found errors**
   - Run `create_index.py` first to generate indices

4. **Timeout errors**
   - Increase timeout in `run_all_tests.py` if needed
   - Check system resources and Ollama performance

### Debug Mode

To run tests with more verbose output, modify the scripts to include debug prints or run them individually with error handling.

## Customization

### Adding New Tests

1. Create new test script following the pattern in `comprehensive_test.py`
2. Add test to `run_all_tests.py` test sequence
3. Update this guide with new test descriptions

### Modifying Test Queries

Edit the `test_queries` lists in the respective scripts to test different scenarios.

### Adjusting Performance Thresholds

Modify the scoring criteria in `comprehensive_test.py` to match your requirements.

## Report Generation

The test suite generates JSON reports in the `test_results/` directory with:
- Timestamp of execution
- Individual test results
- Performance metrics
- Quality assessments
- Recommendations for improvement

Use these reports to track system performance over time and identify areas for optimization.
