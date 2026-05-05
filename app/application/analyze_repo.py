from app.ports.github_port import GitHubPort
from app.ports.llm_port import LLMPort

from app.domain.scoring import compute_repo_score
from app.domain.prompt import build_prompt
from app.domain.models import RepoData

class AnalyzeRepoUseCase:
    def __init__(self, github_port: GitHubPort, llm_port: LLMPort):
        self.github = github_port
        self.llm = llm_port

    def extract_owner_repo(self, url: str):
        parts = url.rstrip("/").split("/")
        return parts[-2], parts[-1]

    async def execute(self, url: str):
        # 1. Extract repo info
        owner, repo = self.extract_owner_repo(url)

        # 2. Fetch repo (via port)
        data = await self.github.fetch_repo(owner, repo)

        # 3. Convert to domain model
        repo_data = RepoData(
            name=data["name"],
            full_name=data["full_name"],
            description=data.get("description"),
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            language=data.get("language"),
            open_issues=data["open_issues_count"]
        )

        # 4. Compute scores (domain)
        scores = compute_repo_score(repo_data)

        # 5. Build prompt (domain)
        prompt = build_prompt(repo_data, scores)

        # 6. Call LLM (via port)
        ai_output = self.llm.analyze(prompt)

        # 7. Return final result
        return {
            "repo": repo_data,
            "scores": scores,
            "ai": ai_output
        }
    