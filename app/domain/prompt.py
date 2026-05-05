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
