import httpx

GITHUB_API = "https://api.github.com/repos"

async def fetch_repo(owner: str, repo: str):
    url = f"{GITHUB_API}/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise Exception("GitHub API error")

    return response.json()
