import os
from dotenv import load_dotenv
from pymilvus import connections
import openai

load_dotenv()

def test_nvidia():
    """Test NVIDIA NIM"""
    try:
        api_key = os.getenv('NVIDIA_API_KEY')
        if not api_key or api_key == "paste-your-key-here":
            print("❌ NVIDIA API key not set in .env file")
            return False
        
        client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        # Quick test
        response = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[{"role": "user", "content": "Say 'test successful' and nothing else"}],
            max_tokens=10
        )
        
        print("✅ NVIDIA NIM connection successful")
        print(f"   Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ NVIDIA NIM failed: {e}")
        return False

def test_milvus():
    """Test Milvus"""
    try:
        connections.connect(
            alias="default",
            host="localhost",
            port="19530"
        )
        print("✅ Milvus connection successful")
        connections.disconnect("default")
        return True
    except Exception as e:
        print(f"❌ Milvus failed: {e}")
        print(f"   Make sure Docker is running: docker ps")
        return False

def test_arxiv():
    """Test arXiv access"""
    try:
        import arxiv
        search = arxiv.Search(
            query="machine learning",
            max_results=1
        )
        results = list(search.results())
        if results:
            print("✅ arXiv API accessible")
            print(f"   Test paper: {results[0].title[:50]}...")
            return True
        return False
    except Exception as e:
        print(f"❌ arXiv failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Local Setup...\n")
    
    nvidia_ok = test_nvidia()
    print()
    milvus_ok = test_milvus()
    print()
    arxiv_ok = test_arxiv()
    
    print("\n" + "="*60)
    if nvidia_ok and milvus_ok and arxiv_ok:
        print("🎉 ALL TESTS PASSED! Ready to build!")
        print("\nNext: We'll start implementing the agent!")
    else:
        print("❌ Fix the failed tests above, then run again")
    print("="*60)