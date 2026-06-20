import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import (
    get_user_data,
    get_user_repos
)

from src.analytics import (
    get_total_stars,
    get_total_forks,
    get_top_repo,
    get_language_breakdown,
    get_top_starred_repos,
    get_repo_creation_trend
)

st.set_page_config(
    page_title="GitHub Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GitHub Analytics Dashboard")

username = st.text_input(
    "GitHub Username",
    value="torvalds"
)

if st.button("Analyze"):

    user = get_user_data(username)
    repos = get_user_repos(username)

    if user is None:
        st.error("User not found")
        st.stop()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(user["avatar_url"], width=150)

    with col2:
        st.subheader(
            user["name"] if user["name"] else username
        )

        st.write(
            user["bio"] if user["bio"]
            else "No bio available"
        )

        st.write(
            f"Followers: {user['followers']}"
        )

        st.write(
            f"Public Repositories: {user['public_repos']}"
        )

    total_stars = get_total_stars(repos)
    total_forks = get_total_forks(repos)
    top_repo = get_top_repo(repos)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⭐ Total Stars",
        total_stars
    )

    c2.metric(
        "🍴 Total Forks",
        total_forks
    )

    c3.metric(
        "📦 Repositories",
        len(repos)
    )

    c4.metric(
        "🏆 Top Repo",
        top_repo["name"] if top_repo else "-"
    )

    st.divider()

    st.subheader(
        "💻 Language Distribution"
    )

    language_data = get_language_breakdown(repos)

    if language_data:

        lang_df = pd.DataFrame({
            "Language": list(language_data.keys()),
            "Count": list(language_data.values())
        })

        fig = px.pie(
            lang_df,
            names="Language",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader(
        "⭐ Top Repositories"
    )

    repo_df = get_top_starred_repos(repos)

    fig = px.bar(
        repo_df,
        x="Repository",
        y="Stars",
        color="Stars"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "📈 Repository Growth"
    )

    trend_df = get_repo_creation_trend(repos)

    fig = px.line(
        trend_df,
        x="date",
        y="count",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "📋 Repository Details"
    )

    repo_table = pd.DataFrame([
        {
            "Repository": repo["name"],
            "Language": repo["language"],
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"]
        }
        for repo in repos
    ])

    st.dataframe(
        repo_table,
        use_container_width=True
    )