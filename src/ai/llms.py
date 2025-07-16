# File: src/ai/llms.py

import os
import subprocess
import time
import json
import uuid
from pathlib import Path
from typing import Optional, List

import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# —— Toggle between API and Cluster via env var —— #
USE_CLUSTER = os.getenv("USE_CLUSTER", "0") == "1"
SAVE_MODELS = int(os.getenv("SAVE_MODELS", "0"))

# —— Cluster / SLURM settings —— #
PARTITION    = os.getenv("CLUSTER_PARTITION",       "p_48G")
GPUS         = os.getenv("CLUSTER_GPUS",            "1")
CPUS         = os.getenv("CLUSTER_CPUS_PER_TASK",   "8")
MEM          = os.getenv("CLUSTER_MEM",             "16G")
BASHRC       = os.getenv("BASHRC_PATH",             "~/.bashrc")
CONDA_INIT   = os.getenv("CONDA_INIT_PATH",         "~/miniconda3/etc/profile.d/conda.sh")
CONDA_ENV    = os.getenv("CLUSTER_CONDA_ENV",       "llm-env")

# —— Paths for cluster‐helper scripts & outputs —— #
AI_DIR   = Path(__file__).parent
DATA_DIR = Path(os.getenv("DATA_DIR_PATH", AI_DIR.parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

def query_llm_cluster(prompt: str, model: str, save_models: int = 0) -> str:
    """
    Submit a SLURM batch job that runs run_llm_query_cluster.py with the specified prompt and model,
    then wait for it to complete and read the output JSON.
    """
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
            f"--prompt '{prompt}' "
            f"--output \"{out_json}\" "
            f"--cache_dir \"{cache_dir}\" "
            f"--save-models {save_models} "
            f"--token \"$HF_TOKEN\""
        )
    ]
    script_content = "\n".join(lines) + "\n"
    script_sh.write_text(script_content, encoding='utf-8', newline='\n')

    # submit job
    job_id = subprocess.check_output(['sbatch', str(script_sh)]).decode().strip().split()[-1]
    # wait for completion
    while True:
        if job_id not in subprocess.check_output(['squeue', '-j', job_id]).decode():
            break
        time.sleep(0.1)

    if not out_json.exists():
        raise FileNotFoundError(f"Output missing: {out_json}")
    data = json.loads(out_json.read_text(encoding='utf-8'))
    return data.get('choices', [{}])[0].get('text', '')

class ModelConfig:
    """
    Configuration class for OpenAI models with structured output support,
    extended to optionally dispatch to HuggingFace on a SLURM cluster.
    """
    MIN_CHUNK_SIZE = 140

    def __init__(self):
        self.openai_client = None
        self.encoder       = None
        self.use_cluster   = USE_CLUSTER
        self.save_models   = SAVE_MODELS
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize OpenAI client and tokenizer."""
        openai_key      = os.getenv("OPENAI_KEY")
        openai_endpoint = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
        if openai_key:
            self.openai_client = OpenAI(
                api_key=openai_key,
                base_url=openai_endpoint
            )
        try:
            self.encoder = tiktoken.get_encoding("o200k_base")
        except Exception:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def get_model_config(self) -> dict:
        """Get the appropriate model configuration for API calls."""
        if not self.openai_client:
            raise Exception("No OpenAI client available – check OPENAI_KEY")
        custom = os.getenv("CUSTOM_MODEL")
        if custom:
            return {
                "client":            self.openai_client,
                "model":             custom,
                "structured_outputs": True,
                "reasoning_effort":  None
            }
        return {
            "client":            self.openai_client,
            "model":             "o3-mini",
            "structured_outputs": True,
            "reasoning_effort":  "medium"
        }

    def generate_completion(
        self,
        messages:        List[dict],
        response_format: Optional[dict] = None,
        **kwargs
    ) -> dict:
        """
        If `use_cluster` is True, send the entire prompt to the HuggingFace SLURM job.
        Otherwise, use the OpenAI API with structured-output support.
        """
        # Flatten chat into a single prompt
        prompt_text = "\n".join(m["content"] for m in messages)
        # Append JSON-schema instructions if needed
        if response_format and response_format.get("json_schema"):
            prompt_text += "\n\nReturn ONLY JSON matching this schema:\n"
            prompt_text += json.dumps(response_format["json_schema"], indent=2)

        if self.use_cluster:
            # Run HF locally via SLURM
            raw = query_llm_cluster(prompt_text, self.get_model_config()["model"], self.save_models)
            # Wrap into a ChatCompletion‐like object
            class Msg: pass
            class Ch:  pass
            class Cmp: pass
            msg = Msg(); setattr(msg, "content", raw)
            ch  = Ch();  setattr(ch,  "message", msg)
            cmp = Cmp(); setattr(cmp, "choices", [ch])
            return cmp

        # FALLBACK: OpenAI API path
        config = self.get_model_config()
        params = {
            "model":    config["model"],
            "messages": messages,
            **kwargs
        }
        if response_format and config["structured_outputs"]:
            params["response_format"] = response_format
        if config["reasoning_effort"] and "o3" in config["model"]:
            params["reasoning_effort"] = config["reasoning_effort"]
        return config["client"].chat.completions.create(**params)


# Keep the old name for compatibility
_model_config_instance = ModelConfig()
