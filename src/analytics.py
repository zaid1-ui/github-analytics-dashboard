from collections import Counter
import pandas as pd


def get_total_stars(repos):
    return sum(
        repo["stargazers_count"]
        for repo in repos
    )


def get_total_forks(repos):
    return sum(
        repo["forks_count"]
        for repo in repos
    )


def get_language_distribution(repos):

    languages = []

    for repo in repos:

        if repo["language"]:
            languages.append(
                repo["language"]
            )

    return dict(
        Counter(languages)
    )


def get_top_repo(repos):

    if not repos:
        return None

    return max(
        repos,
        key=lambda repo: repo["stargazers_count"]
    )


def get_repo_creation_trend(repos):

    if not repos:
        return pd.DataFrame()

    dates = [
        repo["created_at"][:10]
        for repo in repos
    ]

    df = pd.DataFrame({
        "date": pd.to_datetime(dates)
    })

    trend = (
        df.groupby(
            df["date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Repositories")
    )

    trend["date"] = trend["date"].astype(str)

    return trend