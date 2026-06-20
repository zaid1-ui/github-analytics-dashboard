import streamlit as st
import pandas as pd
import plotly.express as px

from src.github_api import get_user, get_user_repos
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

st.title("📊 GitHub Developer Analytics Dashboard")

username = st.text_input(
    "Enter GitHub Username",
    value="torvalds"
)

@st.cache_data(ttl=3600)
def load_user(username):
    return get_user(username)

@st.cache_data(ttl=3600)
def load_repos(username):
    return get_user_repos(username)

if username:

    with st.spinner("Fetching GitHub data..."):
        user = load_user(username)

    if not user:
        st.error("GitHub user not found")
        st.stop()

    repos = load_repos(username)

    st.subheader("👤 Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.image(user["avatar_url"], width=150)

    with col2:
        st.write(f"**Name:** {user.get('name', 'N/A')}")
        st.write(f"**Followers:** {user['followers']}")
        st.write(f"**Following:** {user['following']}")
        st.write(f"**Public Repositories:** {user['public_repos']}")

    total_stars = get_total_stars(repos)
    total_forks = get_total_forks(repos)
    top_repo = get_top_repo(repos)

    st.subheader("📈 Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("⭐ Total Stars", total_stars)
    c2.metric("🍴 Total Forks", total_forks)

    if top_repo:
        c3.metric(
            "🏆 Top Repository",
            top_repo["name"]
        )

    st.subheader("💻 Language Breakdown")

    languages = get_language_breakdown(repos)

    if languages:
        lang_df = pd.DataFrame(
            {
                "Language": languages.keys(),
                "Count": languages.values()
            }
        )

        fig = px.pie(
            lang_df,
            names="Language",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("⭐ Top Starred Repositories")

    top_repos_df = get_top_starred_repos(repos)

    if not top_repos_df.empty:

        fig = px.bar(
            top_repos_df,
            x="Repository",
            y="Stars",
            color="Stars"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            top_repos_df,
            use_container_width=True
        )

    st.subheader("📅 Repository Creation Trend")

    trend_df = get_repo_creation_trend(repos)

    if not trend_df.empty:

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

st.markdown("---")

st.markdown("""
### GitHub Developer Analytics Dashboard

Built with:
- Python
- Streamlit
- GitHub REST API
- Plotly

Created by Your Name
""")