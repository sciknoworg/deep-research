import os
from datetime import date
import requests
from llms import ModelConfig
from prompt_utils import trim_prompt

def get_location_from_ip() -> str:
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "")
            country = data.get("country", "")
            return f"{city}, {country}" if city else country
    except Exception as e:
        print(f"Location error: {e}")
    return "unknown"

def get_current_date() -> str:
    return date.today().strftime("%B %d, %Y")

def main():
    """Test structured output + prompt trimming with user-specified model."""

    # Prompt for model input
    user_model = input("Enter an OpenAI model to use (press Enter to use default 'o3-mini'): ").strip()
    if user_model:
        os.environ["CUSTOM_MODEL"] = user_model  # override environment variable

    config = ModelConfig()

    location = get_location_from_ip()
    today = get_current_date()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides weather information in JSON format based on location and date."
        },
        {
            "role": "user",
            "content": f"What's the weather like in {location} on {today}?"
        }
    ]

    # Structured output format (JSON Schema)
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "weather_response",
            "schema": {
                "type": "object",
                "properties": {
                    "weather": {"type": "string"},
                    "temperature": {"type": "number"},
                    "conditions": {"type": "string"}
                },
                "required": ["weather", "conditions"],
                "additionalProperties": False
            }
        }
    }

    try:
        response = config.generate_completion(
            messages=messages,
            response_format=response_format
        )

        print(f"\n=== Location: {location}")
        print(f"=== Date: {today}")
        print("\n=== AI Response ===")
        print(response.choices[0].message.content)

        long_prompt = "This is a very long prompt. " * 1000
        trimmed = trim_prompt(long_prompt, context_size=100)
        print(f"\nTrimmed prompt example:")
        print(f"Original length: {len(long_prompt)}")
        print(f"Trimmed length: {len(trimmed)}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
