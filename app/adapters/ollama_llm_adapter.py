from app.ports.llm_port import LLMPort
import requests
import os
import json


class OllamaLLMAdapter(LLMPort):

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    def analyze(self, prompt: str, model: str = "llama3.2:3b"):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")

        data = response.json()

        content = data["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON from model",
                "raw_output": content
            }