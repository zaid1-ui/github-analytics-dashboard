from collections import Counter


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