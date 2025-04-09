import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json;charset=utf-8"
}

def search_movie(title):
    url = f"{BASE_URL}/search/movie"
    params = {"query": title}
    print(f"Searching TMDB for: {title}")  # Add this line

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"TMDB search failed for '{title}': {response.status_code}")
        return None

    results = response.json().get("results", [])
    if results:
        print(f"Found '{title}' as: {results[0]['title']} (ID: {results[0]['id']})")
        return results[0]["id"]

    print(f"No results for '{title}'")
    return None


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}

def get_recommendations_for_movie(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    return _fetch_tmdb_list(url)

def get_similar_movies(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/similar"
    return _fetch_tmdb_list(url)

def _fetch_tmdb_list(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []
