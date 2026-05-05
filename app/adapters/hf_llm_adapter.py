from app.ports.llm_port import LLMPort
import os
import requests
import json

API_URL = "https://router.huggingface.co/v1/chat/completions"

class HuggingFaceLLMAdapter(LLMPort):
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
            "Content-Type": "application/json"
        }

    def analyze(self, prompt: str, model: str = "deepseek-ai/DeepSeek-V4-Flash:novita"):
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }

        response = requests.post(API_URL, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"HF API error: {response.text}")

        data = response.json()

        content = data["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
        # fallback safety (very important in real systems)
            return {
                "error": "Invalid JSON from model",
                "raw_output": content
            }
