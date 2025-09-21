from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
import pickle
import os
import time

def create_vector_index(model_name="llama3.2"):
    """Create and save vector index from the dataset with timing measurements"""
    
    print(f"Starting indexing process with model: {model_name}")
    start_time = time.time()
    
    # Create a TextLoader object
    loader = TextLoader("dataset/rentals.csv")
    loader_time = time.time()
    print(f"Data loading completed in {loader_time - start_time:.2f} seconds")
  
    # Create an OllamaEmbeddings object
    embeddings = OllamaEmbeddings(model=model_name)
    embeddings_time = time.time()
    print(f"Embeddings model initialization completed in {embeddings_time - loader_time:.2f} seconds")
    
    # Create a VectorstoreIndexCreator object
    index_creator = VectorstoreIndexCreator(embedding=embeddings)

    # Call from_loaders method
    print("Creating vector index...")
    index_creation_start = time.time()
    index = index_creator.from_loaders([loader])
    index_creation_end = time.time()
    print(f"Vector index creation completed in {index_creation_end - index_creation_start:.2f} seconds")
    
    # Save the index to disk
    os.makedirs("saved_index", exist_ok=True)
    save_start = time.time()
    with open(f"saved_index/vector_index_{model_name.replace('.', '_')}_rentals.pkl", "wb") as f:
        pickle.dump(index, f)
    save_end = time.time()
    print(f"Index saving completed in {save_end - save_start:.2f} seconds")
    
    total_time = time.time() - start_time
    print(f"Total indexing time: {total_time:.2f} seconds")
    print("Indexing document in vector store completed!")
    
    return total_time

def test_multiple_models():
    """Test indexing with different models and compare timing"""
    models = ["llama3.2", "llama3.1", "nomic-embed-text"]
    results = {}
    
    print("=" * 60)
    print("TESTING MULTIPLE MODELS FOR INDEXING PERFORMANCE")
    print("=" * 60)
    
    for model in models:
        try:
            print(f"\nTesting model: {model}")
            print("-" * 40)
            duration = create_vector_index(model)
            results[model] = duration
        except Exception as e:
            print(f"Error with model {model}: {e}")
            results[model] = None
    
    print("\n" + "=" * 60)
    print("INDEXING PERFORMANCE COMPARISON")
    print("=" * 60)
    for model, duration in results.items():
        if duration:
            print(f"{model:20}: {duration:.2f} seconds")
        else:
            print(f"{model:20}: FAILED")
    
    return results

if __name__ == "__main__":
    # Run single model test
    create_vector_index()
    
    # Uncomment to test multiple models
    # test_multiple_models()
