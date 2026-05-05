from fastapi import FastAPI

from app.application.analyze_repo import AnalyzeRepoUseCase
from app.adapters.github_adapter import GitHubAdapter
from app.adapters.hf_llm_adapter import HuggingFaceLLMAdapter
from app.domain.models import RepoRequest

app = FastAPI()

# Create real implementations (ADAPTERS)
github_adapter = GitHubAdapter()
llm_adapter = HuggingFaceLLMAdapter()

# Inject them into the use case
use_case = AnalyzeRepoUseCase(
    github_port=github_adapter,
    llm_port=llm_adapter
)

@app.post("/repo/analyze")
async def analyze_repo(request: RepoRequest):
    result = await use_case.execute(request.url)
    return result
