# File: src/ai/run_llm_query_cluster.py

import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--prompt', required=True, nargs=argparse.REMAINDER)
    parser.add_argument('--output', required=True)
    parser.add_argument('--cache_dir', default=None)
    args = parser.parse_args()

    prompt = ' '.join(args.prompt).strip()
    # Download/Load Model in gemeinsamen Cache-Ordner
    tokenizer = AutoTokenizer.from_pretrained(args.model, cache_dir=args.cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16,
        device_map='auto',
        cache_dir=args.cache_dir
    )

    gen = pipeline('text-generation', model=model, tokenizer=tokenizer, max_new_tokens=256)
    out = gen(prompt)
    text = out[0]['generated_text']

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'choices': [{'text': text}]}, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
