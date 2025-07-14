# File: src/ai/llms.py

import os
import subprocess
import time
import json
import uuid
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List
import tiktoken
from openai import OpenAI

load_dotenv()

PARTITION   = os.getenv('CLUSTER_PARTITION', 'p_48G')
GPUS        = os.getenv('CLUSTER_GPUS', '1')
CPUS        = os.getenv('CLUSTER_CPUS_PER_TASK', '8')
MEM         = os.getenv('CLUSTER_MEM', '16G')
BASHRC      = os.getenv('BASHRC_PATH', '~/.bashrc')
CONDA_INIT  = os.getenv('CONDA_INIT_PATH', '~/miniconda3/etc/profile.d/conda.sh')
CONDA_ENV   = os.getenv('CLUSTER_CONDA_ENV', 'llm-env')

AI_DIR      = Path(__file__).parent
DATA_DIR    = Path(os.getenv('DATA_DIR_PATH', AI_DIR.parent / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)

def query_llm(prompt, model: str, save_models: int = 0) -> str:
    if isinstance(prompt, (list, tuple)):
        prompt_text = "\n".join(str(p) for p in prompt)
    else:
        prompt_text = str(prompt)
    safe = prompt_text.replace('"', '\\"')

    uid       = uuid.uuid4().hex[:8]
    out_json  = DATA_DIR / f"llm_{uid}.json"
    script_sh = DATA_DIR / f"llm_job_{uid}.sh"
    cache_dir = os.getenv('MODEL_CACHE_DIR') or str(AI_DIR.parent / 'models')

    lines = [
        "#!/bin/bash",
        f"#SBATCH --job-name=llm_{uid}",
        f"#SBATCH --output={DATA_DIR}/llm_{uid}.out",
        f"#SBATCH --error={DATA_DIR}/llm_{uid}.err",
        f"#SBATCH --partition={PARTITION}",
        f"#SBATCH --gres=gpu:{GPUS}",
        f"#SBATCH --cpus-per-task={CPUS}",
        f"#SBATCH --mem={MEM}",
        "",
        f"source {BASHRC}",
        f"source {CONDA_INIT}",
        f"conda activate {CONDA_ENV}",
        "",
        (
            f"python {AI_DIR}/run_llm_query_cluster.py "
            f"--model \"{model}\" "
            f"--prompt \"{safe}\" "
            f"--output \"{out_json}\" "
            f"--cache_dir \"{cache_dir}\" "
            f"--save-models {save_models} "
            f"--token \"$HF_TOKEN\""
        )
    ]

    content = "\n".join(lines).replace("\r", "") + "\n"
    with open(script_sh, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    job_id = subprocess.check_output(['sbatch', str(script_sh)]).decode().strip().split()[-1]

    while True:
        if job_id not in subprocess.check_output(['squeue', '-j', job_id]).decode():
            break
        time.sleep(0.1)

    if not out_json.exists():
        raise FileNotFoundError(f"Output missing: {out_json}")
    data = json.loads(out_json.read_text(encoding='utf-8'))
    return data.get('choices', [{}])[0].get('text', '')

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
