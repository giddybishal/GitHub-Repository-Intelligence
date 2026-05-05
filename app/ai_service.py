import os
import requests
import json

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
    "Content-Type": "application/json"
}


def build_prompt(repo, scores):
    return f"""
You are a strict JSON generator.

Return ONLY valid JSON. No markdown. No explanation.

Schema:
{{
  "summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "audience": "string",
  "verdict": "string"
}}

Repository:
Name: {repo.full_name}
Description: {repo.description}
Language: {repo.language}
Stars: {repo.stars}
Forks: {repo.forks}

Scores:
- Popularity: {scores.popularity_score}
- Activity: {scores.activity_score}
- Health: {scores.health_score}
- Final: {scores.final_score}
"""


def get_ai_analysis(prompt: str, model: str = "deepseek-ai/DeepSeek-V4-Flash:novita"):
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

    response = requests.post(API_URL, headers=HEADERS, json=payload)

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
