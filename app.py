import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import (
    get_user,
    get_repos,
    get_repo,
    get_contributors,
    get_languages
)

from src.analytics import (
    get_language_stats,
    get_top_starred_repos
)

from src.repo_analytics import (
    contributor_dataframe,
    language_dataframe,
    calculate_health_score
)

st.set_page_config(
    page_title="GitHub Analytics Dashboard",
    layout="wide"
)

st.title(
    "🚀 GitHub Developer Analytics Dashboard"
)

# ----------------------------------
# USER ANALYTICS
# ----------------------------------

st.header("👤 User Analytics")

username = st.text_input(
    "GitHub Username",
    placeholder="torvalds"
)

if st.button("Analyze User"):

    user = get_user(username)

    if "message" in user:

        st.error("User not found")

    else:

        repos = get_repos(username)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Followers",
            user["followers"]
        )

        c2.metric(
            "Following",
            user["following"]
        )

        c3.metric(
            "Public Repos",
            user["public_repos"]
        )

        c4.metric(
            "Created",
            user["created_at"][:10]
        )

        st.subheader("Profile")

        st.write(
            f"**Name:** {user.get('name')}"
        )

        st.write(
            f"**Bio:** {user.get('bio')}"
        )

        language_stats = get_language_stats(
            repos
        )

        if language_stats:

            lang_df = pd.DataFrame(
                {
                    "Language":
                    language_stats.keys(),

                    "Count":
                    language_stats.values()
                }
            )

            fig = px.pie(
                lang_df,
                names="Language",
                values="Count",
                title="Language Usage"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        top_repos = get_top_starred_repos(
            repos
        )

        repo_df = pd.DataFrame(
            [
                {
                    "Repository":
                    repo["name"],

                    "Stars":
                    repo["stargazers_count"]
                }
                for repo in top_repos
            ]
        )

        fig2 = px.bar(
            repo_df,
            x="Repository",
            y="Stars",
            title="Top Starred Repositories"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ----------------------------------
# REPOSITORY ANALYTICS
# ----------------------------------

st.divider()

st.header("📦 Repository Analytics")

repository = st.text_input(
    "Repository",
    placeholder="microsoft/vscode"
)

if st.button("Analyze Repository"):

    try:

        owner, repo = repository.split("/")

        repo_data = get_repo(
            owner,
            repo
        )

        contributors = get_contributors(
            owner,
            repo
        )

        languages = get_languages(
            owner,
            repo
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Stars",
            repo_data["stargazers_count"]
        )

        c2.metric(
            "Forks",
            repo_data["forks_count"]
        )

        c3.metric(
            "Open Issues",
            repo_data["open_issues_count"]
        )

        c4.metric(
            "Watchers",
            repo_data["watchers_count"]
        )

        health_score = calculate_health_score(
            repo_data["stargazers_count"],
            repo_data["forks_count"],
            len(contributors),
            repo_data["open_issues_count"]
        )

        st.success(
            f"Repository Health Score: {health_score}"
        )

        contributor_df = (
            contributor_dataframe(
                contributors[:10]
            )
        )

        if not contributor_df.empty:

            fig3 = px.bar(
                contributor_df,
                x="Contributor",
                y="Contributions",
                title="Top Contributors"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        lang_df = language_dataframe(
            languages
        )

        if not lang_df.empty:

            fig4 = px.pie(
                lang_df,
                names="Language",
                values="Bytes",
                title="Repository Language Distribution"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

    except Exception:

        st.error(
            "Repository format should be owner/repository"
        )