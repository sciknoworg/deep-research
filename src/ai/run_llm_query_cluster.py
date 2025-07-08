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
    parser.add_argument('--token', default=os.getenv('HF_TOKEN'))
    args = parser.parse_args()

    prompt = ' '.join(args.prompt).strip()
    token  = args.token
    tokenizer = AutoTokenizer.from_pretrained(
        args.model, cache_dir=args.cache_dir, use_auth_token=token, trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model, cache_dir=args.cache_dir, torch_dtype=torch.float16, device_map='auto', use_auth_token=token, trust_remote_code=True
    )
    if args.save_models:
        d= Path('models')/args.model.replace('/','_'); d.mkdir(exist_ok=True)
        tokenizer.save_pretrained(d)
        model.save_pretrained(d)
    gen = pipeline('text-generation', model=model, tokenizer=tokenizer, max_new_tokens=256)
    out=gen(prompt)
    txt=out[0]['generated_text']
    o=Path(args.output); o.parent.mkdir(exist_ok=True)
    o.write_text(json.dumps({'choices':[{'text':txt}]}, ensure_ascii=False, indent=2))

if __name__=='__main__':
    main()