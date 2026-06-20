import requests

BASE_URL = "https://api.github.com"


def get_user_data(username):
    response = requests.get(f"{BASE_URL}/users/{username}")

    if response.status_code == 200:
        return response.json()

    return None


def get_user_repos(username):
    response = requests.get(
        f"{BASE_URL}/users/{username}/repos?per_page=100"
    )

    if response.status_code == 200:
        return response.json()

    return []