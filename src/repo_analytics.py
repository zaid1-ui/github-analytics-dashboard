import pandas as pd


def calculate_repo_score(repo):

    stars = repo["stargazers_count"]
    forks = repo["forks_count"]
    watchers = repo["watchers_count"]
    issues = repo["open_issues_count"]

    score = (
        stars * 5
        + forks * 3
        + watchers
        - issues
    )

    return score


def build_repo_ranking(repos):

    data = []

    for repo in repos:

        data.append(
            {
                "Repository": repo["name"],
                "Stars": repo["stargazers_count"],
                "Forks": repo["forks_count"],
                "Watchers": repo["watchers_count"],
                "Issues": repo["open_issues_count"],
                "Score": calculate_repo_score(repo)
            }
        )

    df = pd.DataFrame(data)

    if not df.empty:

        df = df.sort_values(
            by="Score",
            ascending=False
        )

    return df


def get_developer_score(repos):

    total_score = 0

    for repo in repos:
        total_score += calculate_repo_score(repo)

    return total_score