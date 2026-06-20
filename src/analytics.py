from collections import Counter
import pandas as pd


def get_total_stars(repos):
    return sum(repo["stargazers_count"] for repo in repos)


def get_total_forks(repos):
    return sum(repo["forks_count"] for repo in repos)


def get_total_issues(repos):
    return sum(repo["open_issues_count"] for repo in repos)


def get_language_breakdown(repos):

    languages = []

    for repo in repos:
        if repo.get("language"):
            languages.append(repo["language"])

    return Counter(languages)


def get_top_repo(repos):

    if not repos:
        return None

    return max(
        repos,
        key=lambda x: x["stargazers_count"]
    )


def get_top_starred_repos(repos):

    sorted_repos = sorted(
        repos,
        key=lambda x: x["stargazers_count"],
        reverse=True
    )

    return pd.DataFrame([
        {
            "Repository": repo["name"],
            "Stars": repo["stargazers_count"]
        }
        for repo in sorted_repos[:10]
    ])


def get_repo_creation_trend(repos):

    dates = [
        repo["created_at"][:10]
        for repo in repos
    ]

    if not dates:
        return pd.DataFrame()

    df = pd.DataFrame({
        "date": pd.to_datetime(dates)
    })

    trend = (
        df.groupby(df["date"].dt.to_period("M"))
        .size()
        .reset_index(name="count")
    )

    trend["date"] = trend["date"].astype(str)

    return trend


def get_topics_distribution(repos):

    topics = []

    for repo in repos:
        repo_topics = repo.get("topics", [])
        topics.extend(repo_topics)

    return dict(Counter(topics))