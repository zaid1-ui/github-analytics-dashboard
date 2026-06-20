# Phase 3 placeholder

def calculate_repo_score(repo):

    stars = repo["stargazers_count"]
    forks = repo["forks_count"]

    return stars + (forks * 2)