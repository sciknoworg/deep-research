import argparse
import json
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--prompt", type=str, default=None)
args = parser.parse_args()

if args.prompt:
    prompt_text = args.prompt
else:
    with open("input.json") as f:
        messages = json.load(f)
    prompt_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])

print("[LLM] Generating from:", prompt_text)

tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForCausalLM.from_pretrained(args.model).to("cuda")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)
out = pipe(prompt_text, max_new_tokens=300)

response_text = out[0]["generated_text"]

with open("output.json", "w") as f:
    json.dump({"response": response_text}, f, indent=2)

print("[LLM] Output written to output.json")
