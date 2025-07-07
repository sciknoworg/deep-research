# File: src/ai/llms.py

import os
import tempfile
import subprocess
import time
from pathlib import Path
from typing import Optional

# Definiere einheitliches Modellverzeichnis!
MODEL_CACHE = "/nfs/home/sandere/deep-research/models"

def call_huggingface_on_cluster(prompt: str, model_name: str, index: Optional[int] = None):
    if index is None:
        index = int(time.time() * 1000) % 1000000000
    data_dir = Path(__file__).parents[1] / "data"
    data_dir.mkdir(exist_ok=True)
    output_file = data_dir / f"output_{index}.json"
    if output_file.exists():
        output_file.unlink()
    log_out = data_dir / f"llm_out_{index}.log"
    log_err = data_dir / f"llm_err_{index}.log"
    escaped = prompt.replace('"', '\\"')
    # ACHTUNG: --cache_dir wird übergeben!
    script = f"""#!/bin/bash
#SBATCH --job-name=llm_job_{index}
#SBATCH --output={log_out}
#SBATCH --error={log_err}
#SBATCH --partition=p_48G
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate llm-env

python {Path(__file__).parent}/run_llm_query_cluster.py \
    --model {model_name} \
    --prompt \"{escaped}\" \
    --output {output_file} \
    --cache_dir {MODEL_CACHE}
"""
    p = tempfile.NamedTemporaryFile(delete=False, suffix=".sh")
    p.write(script.encode())
    p.flush()
    subprocess.run(["sbatch", p.name], check=True)
    print(f"[SLURM] Job submitted: {p.name} -> {output_file}")
    return index
