from app.ports.github_port import GitHubPort
import httpx

GITHUB_API = "https://api.github.com/repos"

class GitHubAdapter(GitHubPort):
    async def fetch_repo(self, owner: str, repo: str):
        url = f"{GITHUB_API}/{owner}/{repo}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise Exception("GitHub API error")

        return response.json()
