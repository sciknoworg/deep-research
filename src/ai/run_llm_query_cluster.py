# File: src/ai/run_llm_query_cluster.py

import argparse
import json
import os
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def main():
    parser = argparse.ArgumentParser(description="Run LLM on SLURM cluster")
    parser.add_argument('--model',       required=True, help='HF model name or path')
    parser.add_argument('--prompt',      required=True, help='Prompt text')
    parser.add_argument('--output',      required=True, help='JSON output path')
    parser.add_argument('--cache_dir',   default=None,
                        help='Project‐local models folder (overrides default src/models)')
    parser.add_argument('--save-models', type=int, default=0, help='Save HF models locally once')
    parser.add_argument('--token',       default=os.getenv('HF_TOKEN'), help='HF access token')
    args = parser.parse_args()

    # 1) Bestimme den Projekt‐Root und den Default‐Cache
    project_root = Path(__file__).parent.parent
    default_cache = project_root / "src" / "models"
    CACHE_DIR = Path(args.cache_dir) if args.cache_dir else default_cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # 2) Lokales Modell‐Verzeichnis für genau diesen repo_id
    local_dir = CACHE_DIR / args.model.replace("/", "_")

    # 3) Wenn schon vorhanden, nur von dort laden (kein Download)
    if local_dir.exists():
        tokenizer = AutoTokenizer.from_pretrained(
            str(local_dir), trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            str(local_dir),
            torch_dtype=torch.bfloat16,
            device_map='auto',
            trust_remote_code=True
        )

    # 4) Sonst: einmal runterladen, dann ggf. speichern
    else:
        # Download in den HF‐Cache unter CACHE_DIR
        tokenizer = AutoTokenizer.from_pretrained(
            args.model,
            cache_dir=str(CACHE_DIR),
            token=args.token,
            trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            cache_dir=str(CACHE_DIR),
            torch_dtype=torch.bfloat16,
            device_map='auto',
            token=args.token,
            trust_remote_code=True
        )
        if args.save_models:
            local_dir.mkdir(parents=True, exist_ok=True)
            tokenizer.save_pretrained(str(local_dir))
            model.save_pretrained(str(local_dir))

    # 5) Generiere Text (Pipeline ohne device‐Override, accelerate shards automatisch)
    gen = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256
    )
    text = gen(args.prompt)[0]['generated_text']

    # 6) Schreibe JSON-Output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({'choices': [{'text': text}]}, ensure_ascii=False),
        encoding='utf-8'
    )

if __name__ == '__main__':
    main()
