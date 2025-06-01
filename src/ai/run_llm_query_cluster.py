import argparse
import json
import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

def get_model_repo(model_key):
    models = {
        "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
        "deepseek": "deepseek-ai/deepseek-llm-7b-chat",
        "zephyr": "HuggingFaceH4/zephyr-7b-beta"
    }
    if model_key not in models:
        raise ValueError(f"Unknown model key '{model_key}'. Choose from: {list(models.keys())}")
    return models[model_key]

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, help="Choose from: mistral, deepseek, zephyr")
parser.add_argument("--prompt", type=str, default=None)
args = parser.parse_args()

model_repo = get_model_repo(args.model)

if args.prompt:
    prompt_text = args.prompt
else:
    with open("data/input.json") as f:
        messages = json.load(f)
    prompt_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])

print("[LLM] Generating from:", prompt_text)

# Modell laden
try:
    tokenizer = AutoTokenizer.from_pretrained(model_repo)
    model = AutoModelForCausalLM.from_pretrained(model_repo, torch_dtype=torch.float16, device_map="auto")
except Exception as e:
    print("[ERROR] Failed to load model:", e)
    exit(1)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)
out = pipe(prompt_text, max_new_tokens=300)

response_text = out[0]["generated_text"]

Path("data").mkdir(exist_ok=True)
with open("data/output.json", "w") as f:
    json.dump({"response": response_text}, f, indent=2)

print("[LLM] Output written to data/output.json")
