from .models import RepoScore

# Repo Scoring Logic
def clamp(value, min_val=0, max_val=100):
    return max(min_val, min(value, max_val))

def calculate_popularity(stars: int, forks: int):
    score = (stars * 0.7) + (forks * 0.3)
    return clamp(score / 10)

def calculate_activity(open_issues: int):
    if open_issues < 10:
        return 80
    elif open_issues < 50:
        return 70
    elif open_issues < 200:
        return 50
    else:
        return 30

def calculate_health(description, language):
    score = 50

    if description:
        score += 20
    if language:
        score += 20

    return clamp(score)

def final_verdict(score):
    if score >= 80:
        return "Excellent project"
    elif score >= 60:
        return "Good project"
    elif score >= 40:
        return "Average project"
    else:
        return "Weak project"
    
def compute_repo_score(repo_data):
    popularity = calculate_popularity(repo_data.stars, repo_data.forks)
    activity = calculate_activity(repo_data.open_issues)
    health = calculate_health(repo_data.description, repo_data.language)

    final = (popularity * 0.4) + (activity * 0.3) + (health * 0.3)

    return RepoScore(
        popularity_score=popularity,
        activity_score=activity,
        health_score=health,
        final_score=round(final, 2),
        verdict=final_verdict(final)
    )
