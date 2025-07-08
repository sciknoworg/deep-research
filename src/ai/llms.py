import os
import tempfile
import subprocess
import time
from pathlib import Path
from typing import Optional

# Shared cache directory for models
MODEL_CACHE = os.getenv('MODEL_CACHE_DIR', '/nfs/home/user/deep-research/models')

def call_huggingface_on_cluster(
    prompt: str,
    model_name: str,
    save_models: int = 0,
    index: Optional[int] = None
) -> int:
    # Lazy-load transformers to avoid startup delay
    from transformers import AutoModel, AutoTokenizer

    if index is None:
        index = int(time.time() * 1000) % 1000000000
    data_dir = Path(__file__).parents[1] / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    output_file = data_dir / f'output_{index}.json'
    output_path = output_file.as_posix()
    # remove existing output
    if output_file.exists():
        output_file.unlink()
    log_out = data_dir / f'llm_out_{index}.log'
    log_err = data_dir / f'llm_err_{index}.log'
    script_path = (Path(__file__).parent / 'run_llm_query_cluster.py').as_posix()
    escaped_prompt = prompt.replace('"', '\"')

    # Create SLURM script content
    script = f'''#!/bin/bash
#SBATCH --job-name=llm_job_{index}
#SBATCH --output={log_out.as_posix()}
#SBATCH --error={log_err.as_posix()}
#SBATCH --partition=p_48G
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

source ~/.bashrc
source ~/miniconda3/etc/profile.d/conda.sh
conda activate llm-env

# Execute the LLM query script
python {script_path} \
  --model "{model_name}" \
  --prompt "{escaped_prompt}" \
  --output "{output_path}" \
  --cache_dir "{MODEL_CACHE}" \
  --save-models {int(save_models)} \
  --token ${{HF_TOKEN}}
'''
    # Write and submit the SLURM job
    p = tempfile.NamedTemporaryFile(delete=False, suffix='.sh')
    p.write(script.encode())
    p.flush()
    subprocess.run(['sbatch', p.name], check=True)
    print(f"[SLURM] Job submitted: {p.name} -> {output_path}")
    return index

# Alias for LLM queries
query_llm = call_huggingface_on_cluster