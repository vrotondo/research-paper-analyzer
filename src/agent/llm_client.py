"""
NVIDIA NIM LLM Client
Connects to llama-3_1-nemotron-nano-8B-v1 via NVIDIA NIM
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class NvidiaLLMClient:
    """Client for NVIDIA NIM inference microservice"""
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
        
        # NVIDIA NIM uses OpenAI-compatible API
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        
        # Model specified in hackathon requirements
        self.model = "meta/llama-3.1-8b-instruct"
    
    def generate_response(self, prompt: str, system_message: str = None, max_tokens: int = 1000) -> str:
        """
        Generate a response from the LLM
        
        Args:
            prompt: User prompt
            system_message: System instruction (optional)
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error calling NVIDIA NIM: {str(e)}")
    
    def stream_response(self, prompt: str, system_message: str = None):
        """
        Stream response from LLM (for better UX)
        
        Args:
            prompt: User prompt
            system_message: System instruction (optional)
            
        Yields:
            Chunks of generated text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            raise Exception(f"Error streaming from NVIDIA NIM: {str(e)}")