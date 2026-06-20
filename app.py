import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import (
    get_user,
    get_repos
)

from src.analytics import (
    get_total_stars,
    get_total_forks,
    get_language_distribution,
    get_top_repo,
    get_repo_creation_trend
)

from src.repo_analytics import (
    build_repo_ranking
)

st.set_page_config(
    page_title="GitHub Analytics Dashboard",
    layout="wide"
)

st.title("🚀 GitHub Developer Analytics Dashboard")

username = st.text_input(
    "GitHub Username",
    "torvalds"
)

if st.button("Analyze"):

    user = get_user(username)

    if not user:
        st.error("User not found")
        st.stop()

    repos = get_repos(username)

    st.success(
        f"Analysis Complete for {username}"
    )

    st.image(
        user["avatar_url"],
        width=150
    )

    st.subheader(user["name"] or username)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Followers",
            user["followers"]
        )

    with col2:
        st.metric(
            "Following",
            user["following"]
        )

    with col3:
        st.metric(
            "Public Repos",
            user["public_repos"]
        )

    with col4:
        st.metric(
            "Account Created",
            user["created_at"][:10]
        )

    st.divider()

    total_stars = get_total_stars(repos)
    total_forks = get_total_forks(repos)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Repositories",
            len(repos)
        )

    with c2:
        st.metric(
            "Total Stars",
            total_stars
        )

    with c3:
        st.metric(
            "Total Forks",
            total_forks
        )

    st.divider()

    repo_df = pd.DataFrame([
        {
            "Repository": repo["name"],
            "Stars": repo["stargazers_count"]
        }
        for repo in repos
    ])

    if not repo_df.empty:

        fig = px.bar(
            repo_df,
            x="Repository",
            y="Stars",
            title="Stars Per Repository"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    languages = get_language_distribution(
        repos
    )

    if languages:

        language_df = pd.DataFrame(
            list(languages.items()),
            columns=[
                "Language",
                "Count"
            ]
        )

        fig2 = px.pie(
            language_df,
            names="Language",
            values="Count",
            title="Language Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    trend_df = get_repo_creation_trend(
        repos
    )

    if not trend_df.empty:

        fig3 = px.line(
            trend_df,
            x="date",
            y="Repositories",
            markers=True,
            title="Repository Creation Trend"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.divider()

    ranking_df = build_repo_ranking(
        repos
    )

    st.subheader(
        "🏆 Repository Leaderboard"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.download_button(
        "📥 Download CSV",
        ranking_df.to_csv(
            index=False
        ),
        "repository_ranking.csv",
        "text/csv"
    )

    st.divider()

    top_repo = get_top_repo(repos)

    if top_repo:

        st.subheader(
            "⭐ Most Starred Repository"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Repository",
                top_repo["name"]
            )

        with c2:
            st.metric(
                "Stars",
                top_repo["stargazers_count"]
            )

        with c3:
            st.metric(
                "Forks",
                top_repo["forks_count"]
            )