import argparse
import json
import os
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--prompt', required=True, nargs=argparse.REMAINDER)
    parser.add_argument('--output', required=True)
    parser.add_argument('--cache_dir', default=None)
    parser.add_argument('--save-models', type=int, default=0)
    parser.add_argument('--token', type=str, default=os.getenv('HF_TOKEN'), help='Huggingface access token')
    args = parser.parse_args()
    prompt = ' '.join(args.prompt).strip()
    auth_token = args.token

    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        cache_dir=args.cache_dir,
        use_auth_token=auth_token,
        trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16,
        device_map='auto',
        cache_dir=args.cache_dir,
        use_auth_token=auth_token,
        trust_remote_code=True
    )

    if args.save_models:
        local_dir = Path(__file__).parents[2] / 'models' / args.model.replace('/', '_')
        local_dir.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(local_dir)
        model.save_pretrained(local_dir)

    gen = pipeline(
        'text-generation',
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        use_auth_token=auth_token
    )
    out = gen(prompt)
    text = out[0]['generated_text']

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'choices': [{'text': text}]}, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()