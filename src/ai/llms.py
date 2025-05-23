import os
from typing import Optional, List
import tiktoken
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

class ModelConfig:
    """Configuration class for OpenAI models with structured output support."""
    
    MIN_CHUNK_SIZE = 140
    
    def __init__(self):
        self.openai_client = None
        self.encoder = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize OpenAI client and tokenizer."""
        openai_key = os.getenv('OPENAI_KEY')
        openai_endpoint = os.getenv('OPENAI_ENDPOINT', 'https://api.openai.com/v1')
        
        if openai_key:
            self.openai_client = OpenAI(
                api_key=openai_key,
                base_url=openai_endpoint
            )
        
        # Initialize tokenizer
        try:
            self.encoder = tiktoken.get_encoding('o200k_base')
        except Exception:
            # Fallback to cl100k_base if o200k_base is not available
            self.encoder = tiktoken.get_encoding('cl100k_base')
    
    def get_model_config(self) -> dict:
        """Get the appropriate model configuration."""
        if not self.openai_client:
            raise Exception('No OpenAI client available - check OPENAI_KEY environment variable')
        
        custom_model = os.getenv('CUSTOM_MODEL')
        
        if custom_model:
            return {
                'client': self.openai_client,
                'model': custom_model,
                'structured_outputs': True,
                'reasoning_effort': None
            }
        
        # Default to o3-mini with reasoning effort
        return {
            'client': self.openai_client,
            'model': 'o3-mini',
            'structured_outputs': True,
            'reasoning_effort': 'medium'
        }
    
    def generate_completion(self, 
                          messages: List[dict], 
                          response_format: Optional[dict] = None,
                          **kwargs) -> dict:
        """Generate a completion using the configured model."""
        config = self.get_model_config()
        
        # Prepare parameters
        params = {
            'model': config['model'],
            'messages': messages,
            **kwargs
        }
        
        # Add structured output if provided
        if response_format and config['structured_outputs']:
            params['response_format'] = response_format
        
        # Add reasoning effort for o3 models
        if config['reasoning_effort'] and 'o3' in config['model']:
            params['reasoning_effort'] = config['reasoning_effort']
        
        return config['client'].chat.completions.create(**params)
    

_model_config_instance = ModelConfig()


