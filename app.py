import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import get_user, get_repos
from src.analytics import (
    get_total_stars,
    get_total_forks,
    get_language_distribution,
)
from src.repo_analytics import build_repo_ranking

st.set_page_config(
    page_title="GitHub Analytics Dashboard",
    layout="wide"
)

st.title("🚀 GitHub Analytics Dashboard")

username = st.text_input(
    "Enter GitHub Username",
    "torvalds"
)

if st.button("Analyze"):

    user = get_user(username)
    repos = get_repos(username)

    if "message" in user:
        st.error("User not found")
        st.stop()

    st.success(f"Analyzing {username}")

    total_stars = get_total_stars(repos)
    total_forks = get_total_forks(repos)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Repositories", len(repos))

    with col2:
        st.metric("Stars", total_stars)

    with col3:
        st.metric("Forks", total_forks)

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

    language_data = get_language_distribution(repos)

    if language_data:

        language_df = pd.DataFrame(
            list(language_data.items()),
            columns=["Language", "Count"]
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

    st.subheader("🏆 Repository Leaderboard")

    ranking_df = build_repo_ranking(repos)

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    st.download_button(
        label="📥 Download Ranking CSV",
        data=ranking_df.to_csv(index=False),
        file_name="github_repo_ranking.csv",
        mime="text/csv"
    )

    if not ranking_df.empty:

        st.divider()

        st.subheader("⭐ Top Repository")

        top_repo = ranking_df.iloc[0]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Repository",
                top_repo["Repository"]
            )

        with c2:
            st.metric(
                "Stars",
                int(top_repo["Stars"])
            )

        with c3:
            st.metric(
                "Score",
                int(top_repo["Score"])
            )