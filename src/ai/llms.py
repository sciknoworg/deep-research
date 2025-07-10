# File: src/ai/llms.py

import os
import subprocess
import time
import json
import uuid
from pathlib import Path
from dotenv import load_dotenv

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
