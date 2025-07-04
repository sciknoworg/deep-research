import os
import subprocess
import time
import json
import uuid
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

env = os.environ
PARTITION = env.get('CLUSTER_PARTITION', 'p_48G')
GPUS = env.get('CLUSTER_GPUS', '1')
CPUS = env.get('CLUSTER_CPUS_PER_TASK', '8')
MEM = env.get('CLUSTER_MEM', '16G')
BASHRC = env.get('BASHRC_PATH', '~/.bashrc')
CONDA_INIT = env.get('CONDA_INIT', '~/miniconda3/etc/profile.d/conda.sh')
CONDA_ENV = env.get('CLUSTER_CONDA_ENV', 'llm-env')
AI_DIR = Path(__file__).parent
DATA_DIR = Path(env.get('DATA_DIR_PATH', AI_DIR.parent / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ALIASES = {
    'mistral': 'mistralai/Mistral-7B-Instruct-v0.2',
    'deepseek': 'deepseek-ai/deepseek-llm-7b-chat',
    'zephyr': 'HuggingFaceH4/zephyr-7b-beta',
}

def resolve_model(key: str) -> str:
    return MODEL_ALIASES.get(key, key)


def query_llm(prompt: str, model_key: str = None) -> str:
    model = resolve_model(os.getenv('DEFAULT_MODEL_ALIAS', model_key or 'zephyr'))
    uid = uuid.uuid4().hex[:8]
    out_json = DATA_DIR / f"llm_{uid}.json"
    script_sh = DATA_DIR / f"llm_job_{uid}.sh"

    safe_prompt = prompt.replace('"', '\\"')

    script = f"""#!/bin/bash
#SBATCH --job-name=llm_{uid}
#SBATCH --output={DATA_DIR}/llm_{uid}.out
#SBATCH --error={DATA_DIR}/llm_{uid}.err
#SBATCH --partition={PARTITION}
#SBATCH --gres=gpu:{GPUS}
#SBATCH --cpus-per-task={CPUS}
#SBATCH --mem={MEM}

source {BASHRC}
source {CONDA_INIT}
conda activate {CONDA_ENV}

python {AI_DIR}/run_llm_query_cluster.py --model \"{model}\" --output \"{out_json}\" --prompt \"{safe_prompt}\""""
    script_sh.write_text(script)

    job_id = subprocess.check_output(['sbatch', str(script_sh)]).decode().strip().split()[-1]
    while job_id in subprocess.check_output(['squeue', '-j', job_id]).decode():
        time.sleep(5)

    if not out_json.exists():
        raise FileNotFoundError(f"Output file missing: {out_json}")

    resp = json.loads(out_json.read_text())
    return resp.get('choices', [{}])[0].get('text', '')


class ModelConfig:
    def __init__(self):
        self.model = resolve_model(os.getenv('DEFAULT_MODEL_ALIAS', 'zephyr'))
        self.client = query_llm

    def get_model_config(self):
        return {'model': self.model, 'client': self.client}