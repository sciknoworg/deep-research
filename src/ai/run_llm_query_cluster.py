# File: src/ai/run_llm_query_cluster.py
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    # Accept everything after --prompt as the prompt text
    parser.add_argument('--prompt', required=True, nargs=argparse.REMAINDER)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    # `nargs=REMAINDER` captures all tokens after --prompt
    prompt = ' '.join(args.prompt).strip()

    # Reconstruct full prompt
    prompt = ' '.join(args.prompt)

    # Load model and tokenizer from local cache
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16,
        device_map='auto',
        local_files_only=True
    )
    gen = pipeline('text-generation', model=model, tokenizer=tokenizer, max_new_tokens=256)

    # Generate text
    out = gen(prompt)
    text = out[0]['generated_text']

    # Write output JSON in expected format
    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'choices': [{'text': text}]}, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
