import argparse
import json
import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, default="deepseek-ai/deepseek-llm-7b-chat")
parser.add_argument("--prompt", type=str, default=None)
parser.add_argument("--output", type=str, default="/nfs/home/sandere/deep-research/src/data/output.json")
args = parser.parse_args()

if args.prompt:
    prompt_text = args.prompt
else:
    with open("data/input.json") as f:
        messages = json.load(f)
    prompt_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])

print("[LLM] Generating from:", prompt_text)

# Modell laden
try:
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float16, device_map="auto")
except Exception as e:
    print("[ERROR] Failed to load model:", e)
    exit(1)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
out = pipe(prompt_text, max_new_tokens=300)

response_text = out[0]["generated_text"]

Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)
with open(args.output, "w") as f:  # <-- Verwendung des übergebenen output-Pfads
    json.dump({"response": response_text}, f, indent=2)

print(f"[LLM] Output written to {args.output}")
