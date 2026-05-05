from pydantic import BaseModel
from typing import Optional

class RepoRequest(BaseModel):
    url: str

class RepoData(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    stars: int
    forks: int
    language: Optional[str]
    open_issues: int
    
class RepoScore(BaseModel):
    popularity_score: float
    activity_score: float
    health_score: float
    final_score: float
    verdict: str
    