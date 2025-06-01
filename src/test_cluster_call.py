import asyncio
import json

from ai.llms import call_huggingface_on_cluster, wait_for_output_file
from ai.prompt_utils import trim_prompt


async def main():
    # Einfacher Prompt für Testzwecke
    prompt = trim_prompt("Nenne drei wichtige Eigenschaften von kaffe.")

    # Modellname kann geändert werden, z. B. "mistral" oder "deepseek"
    model_name = "deepseek-ai/deepseek-llm-7b-chat"
    index = 900

    print("[ClusterTest] Sende Prompt an Cluster...")
    call_huggingface_on_cluster(prompt, model_name=model_name, index=index)

    print("[ClusterTest] Warte auf Antwort...")
    result = wait_for_output_file(index=index)

    print("[ClusterTest] Antwort erhalten:")
    print("---")
    try:
        response = result.get("response", "")
        print(json.dumps(json.loads(response), indent=2))
    except Exception:
        print(response)


if __name__ == "__main__":
    asyncio.run(main())