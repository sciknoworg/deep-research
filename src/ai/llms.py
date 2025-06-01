import os
from typing import Optional, List
import tiktoken
from openai import OpenAI
import tempfile
import subprocess
import json
import time

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

def call_huggingface_on_cluster(prompt: str, model_name: str = "deepseek", index: Optional[int] = None):
    if index is None:
        index = uuid.uuid4().int >> 96

    escaped_prompt = prompt.replace('"', '\\"')
    output_path = f"/nfs/home/sandere/deep-research/src/data/output_{index}.json"

    script = f"""#!/bin/bash
#SBATCH --job-name=start-llm
#SBATCH --output=llm_out_{index}.log
#SBATCH --error=llm_err_{index}.log
#SBATCH --partition=p_48G
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate llm-env
python /nfs/home/sandere/deep-research/src/ai/run_llm_query_cluster.py --model {model_name} --prompt \"{escaped_prompt}\" --output {output_path}
"""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".sh") as f:
        f.write(script.encode("utf-8"))
        job_file = f.name

    subprocess.run(["sbatch", job_file])
    print(f"[SLURM] Job submitted: {job_file} -> output_{index}.json")
    return index

def wait_for_output_file(index: int, timeout: int = 120, interval: int = 5):
    output_path = f"/nfs/home/sandere/deep-research/src/data/output_{index}.json"
    waited = 0
    while waited < timeout:
        if os.path.exists(output_path):
            with open(output_path) as f:
                return json.load(f)
        time.sleep(interval)
        waited += interval
    raise TimeoutError(f"Timeout waiting for output file: {output_path}")


