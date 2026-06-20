import pandas as pd


def contributor_dataframe(contributors):

    data = []

    for contributor in contributors:

        data.append(
            {
                "Contributor":
                contributor["login"],

                "Contributions":
                contributor["contributions"]
            }
        )

    return pd.DataFrame(data)


def language_dataframe(languages):

    return pd.DataFrame(
        {
            "Language":
            list(languages.keys()),

            "Bytes":
            list(languages.values())
        }
    )


def calculate_health_score(
    stars,
    forks,
    contributors,
    issues
):

    score = (
        stars * 0.4
        + forks * 0.3
        + contributors * 0.2
        - issues * 0.1
    )

    return round(score, 2)