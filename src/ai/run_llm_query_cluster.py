import argparse
import json
import os
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


def main():
    parser = argparse.ArgumentParser(description="Run LLM on SLURM cluster")
    parser.add_argument('--model',      required=True, help='HuggingFace model name or path')
    parser.add_argument('--prompt',     required=True, help='Prompt text to send')
    parser.add_argument('--output',     required=True, help='Path to JSON output file')
    parser.add_argument('--cache_dir',  default=None, help='HF cache directory')
    parser.add_argument('--save-models',type=int, default=0, help='Whether to save model locally')
    parser.add_argument('--token',      default=os.getenv('HF_TOKEN'), help='HuggingFace access token')
    args = parser.parse_args()

    # 1) Load tokenizer & model
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        cache_dir=args.cache_dir,
        token=args.token,
        trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        cache_dir=args.cache_dir,
        torch_dtype=torch.bfloat16,
        device_map='auto',
        token=args.token,
        trust_remote_code=True
    )

    # 2) Optionally save a pinned copy
    if args.save_models:
        save_dir = Path(args.cache_dir or Path(__file__).parent.parent / 'models') / args.model.replace('/', '_')
        save_dir.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(save_dir)
        model.save_pretrained(save_dir)

    # 3) Build text-generation pipeline (enable sampling, remove invalid stop_token)
    gen = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        num_beams=4,
        early_stopping=True,
        max_new_tokens=1000,
        temperature=0.1,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.2,
        length_penalty=1.3,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2,
        return_full_text=False,
        clean_up_tokenization_spaces=True
    )

    # 4) Generate & dump JSON
    out = gen(args.prompt)
    text = out[0].get('generated_text', '') if isinstance(out, list) else out.get('generated_text', '')
    result = {'choices': [{'text': text}]}
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
