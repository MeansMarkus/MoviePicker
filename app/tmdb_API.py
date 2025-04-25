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
    #print(f"Searching TMDB for: {title}")  

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"TMDB search failed for '{title}': {response.status_code}")
        return None

    results = response.json().get("results", [])
    if results:
        #print(f"Found '{title}' as: {results[0]['title']} (ID: {results[0]['id']})")
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
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    response = requests.get(url, headers=HEADERS)
    #print(f"RECOMMENDATIONS for {movie_id}:", response.status_code)
    try:
        data = response.json()
        #print(data)
    except Exception as e:
        print("Failed to decode JSON:", e)
        return []
    if response.status_code == 200:
        return data.get("results", [])
    return []

def get_similar_movies(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
    response = requests.get(url, headers=HEADERS)
    #print(f"SIMILAR for {movie_id}:", response.status_code)
    try:
        data = response.json()
        #print(data)
    except Exception as e:
        print("Failed to decode JSON:", e)
        return []
    if response.status_code == 200:
        return data.get("results", [])
    return []

def get_content_rating(movie_id: int, country: str = "US") -> str:
    url = f"{BASE_URL}/movie/{movie_id}/release_dates"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return ""
    data = response.json().get("results", [])
    for entry in data:
        if entry.get("iso_3166_1") == country:
            for rel in entry.get("release_dates", []):
                cert = rel.get("certification")
                if cert:
                    return cert
    return ""

def get_genre_list() -> list[str]:
    url = f"{BASE_URL}/genre/movie/list"
    response = requests.get(url, headers=HEADERS, params={"language":"en-US"})
    if response.status_code != 200:
        return []
    data = response.json().get("genres", [])
    return [g.get("name") for g in data if g.get("name")]

def _fetch_tmdb_list(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []
