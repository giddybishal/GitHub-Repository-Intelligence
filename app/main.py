from fastapi import FastAPI
from .models import RepoRequest
from .service import get_repo_data, compute_repo_score
from .ai_service import get_ai_analysis, build_prompt

app = FastAPI()

@app.post("/repo/analyze")
async def analyze_repo(request: RepoRequest):
    repo_data = await get_repo_data(request.url)
    scores = compute_repo_score(repo_data)
    prompt = build_prompt(repo_data, scores)
    ai_output = get_ai_analysis(prompt)

    return {
        "repo": repo_data,
        "analysis": scores,
        "ai": ai_output
    }
