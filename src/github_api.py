import requests

BASE_URL = "https://api.github.com"


def get_user(username):
    response = requests.get(
        f"{BASE_URL}/users/{username}"
    )
    return response.json()


def get_repos(username):
    response = requests.get(
        f"{BASE_URL}/users/{username}/repos"
    )
    return response.json()


def get_repo(owner, repo):
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}"
    )
    return response.json()


def get_contributors(owner, repo):
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/contributors"
    )
    return response.json()


def get_languages(owner, repo):
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/languages"
    )
    return response.json()