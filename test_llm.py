"""
Test NVIDIA NIM LLM Connection
Run this to verify your API key works
"""
from src.agent.llm_client import NvidiaLLMClient


def test_basic_call():
    """Test basic LLM call"""
    print("🔧 Initializing NVIDIA NIM client...")
    
    try:
        client = NvidiaLLMClient()
        print("✅ Client initialized successfully!")
        print(f"📝 Using model: {client.model}")
        
        print("\n🤖 Testing basic prompt...")
        prompt = "Explain what a research paper abstract is in one sentence."
        
        response = client.generate_response(
            prompt=prompt,
            system_message="You are a helpful research assistant."
        )
        
        print(f"\n💬 Response:\n{response}")
        print("\n✅ LLM connection test successful!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    
    return True


def test_streaming():
    """Test streaming response"""
    print("\n" + "="*50)
    print("🔧 Testing streaming response...")
    
    try:
        client = NvidiaLLMClient()
        prompt = "What are the key components of a good research paper?"
        
        print("\n💬 Streaming response:\n")
        
        for chunk in client.stream_response(
            prompt=prompt,
            system_message="You are a helpful research assistant."
        ):
            print(chunk, end="", flush=True)
        
        print("\n\n✅ Streaming test successful!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    print("="*50)
    print("NVIDIA NIM LLM Connection Test")
    print("="*50)
    
    # Test basic call
    if test_basic_call():
        # Test streaming
        test_streaming()
    
    print("\n" + "="*50)
    print("Tests complete!")
    print("="*50)