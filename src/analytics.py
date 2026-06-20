from collections import Counter


def get_language_stats(repos):

    languages = []

    for repo in repos:

        if repo.get("language"):
            languages.append(
                repo["language"]
            )

    return Counter(languages)


def get_top_starred_repos(repos):

    return sorted(
        repos,
        key=lambda x: x["stargazers_count"],
        reverse=True
    )[:10]