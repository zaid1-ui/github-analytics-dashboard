import pandas as pd


def calculate_repo_score(repo):

    stars = repo["stargazers_count"]
    forks = repo["forks_count"]
    watchers = repo["watchers_count"]

    return (
        stars * 5
        + forks * 3
        + watchers
    )


def build_repo_ranking(repos):

    ranking = []

    for repo in repos:

        ranking.append({
            "Repository": repo["name"],
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"],
            "Watchers": repo["watchers_count"],
            "Score": calculate_repo_score(repo)
        })

    df = pd.DataFrame(ranking)

    if not df.empty:

        df = df.sort_values(
            by="Score",
            ascending=False
        )

    return df