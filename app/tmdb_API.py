import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter
 
load_dotenv() # Security: pulls api key from environment variables - secrets aren't hard coded

# Architecture: lone integration point to the TMDB service

API_KEY = os.getenv("TMDB_API_KEY") # Bearer token!

BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json;charset=utf-8"
}

# Reliability: all API requests include a check response.status_code that returns empty lists or logs 
# failure so uncaught exceptions don't crash the app

def search_movie(title):
    """
    Search TMDB for movie by title and return the first match’s ID

    :param title: Movie title to query
    :type title: str
    :return: TMDB movie ID or None if not found
    :rtype: int or None
    """
    url = f"{BASE_URL}/search/movie"
    params = {"query": title}
    #print(f"Searching TMDB for: {title}")  

    # ask TMDB API
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"TMDB search failed for '{title}': {response.status_code}")
        return None

    # top 'limit' results
    results = response.json().get("results", [])
    if results:
        #print(f"Found '{title}' as: {results[0]['title']} (ID: {results[0]['id']})")
        return results[0]["id"]

    print(f"No results for '{title}'")
    return None


def get_movie_details(movie_id):
    """
    Get detailed info for a movie

    :param movie_id: TMDB movie ID
    :type movie_id: int
    :return: JSON details dict or {} on failure
    :rtype: dict
    """
    url = f"{BASE_URL}/movie/{movie_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}

def get_recommendations_for_movie(movie_id):
    """
    Get TMDB recommendations list for a movie

    :param movie_id: TMDB movie ID
    :type movie_id: int
    :return: List of recommendation dicts
    :rtype: list[dict]
    """
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
    """
    Get TMDB “similar movies” list for a movie

    :param movie_id: TMDB movie ID
    :type movie_id: int
    :return: List of similar movie dicts
    :rtype: list[dict]
    """
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
    """
    Get movie’s content rating in the US

    :param movie_id: TMDB movie ID.
    :type movie_id: int
    :param country: ISO country code (default "US").
    :type country: str
    :return: Certification string (e.g. "PG-13") or empty.
    :rtype: str
    """
    url = f"{BASE_URL}/movie/{movie_id}/release_dates"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return ""
    data = response.json().get("results", [])
    # iterate through country entries
    for entry in data:
        if entry.get("iso_3166_1") == country:
            for rel in entry.get("release_dates", []):
                cert = rel.get("certification")
                if cert:
                    return cert
    return ""

def get_genre_list() -> list[str]:
    """
    Get list of all TMDB movie genres

    :return: List of genre names
    :rtype: list[str]
    """
    url = f"{BASE_URL}/genre/movie/list"
    response = requests.get(url, headers=HEADERS, params={"language":"en-US"})
    if response.status_code != 200:
        return []
    data = response.json().get("genres", [])
    return [g.get("name") for g in data if g.get("name")]

def _fetch_tmdb_list(url):
    """
    Helper - get paginated TMDB list results

    :param url: Full TMDB list URL
    :type url: str
    :return: JSON `results` array or []
    :rtype: list[dict]
    """
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

router = APIRouter()

@router.get("/search")
def search_movies_endpoint(q: str, limit: int = 5):
    """
    FastAPI endpoint for movie search

    :param q: Query string
    :type q: str
    :param limit: Maximum results to return
    :type limit: int
    :return: Dict with list of {title, id, year}
    :rtype: dict
    """
    params = {"query": q, "language": "en-US", "page": 1, "include_adult": False}
    #HTTP get to TMDB /search/movie
    resp = requests.get(f"{BASE_URL}/search/movie", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return {"results": []}
    results = resp.json().get("results", [])[:limit]
    # simplified response objects
    return {
        "results": [
            {
                "title": m.get("title"),
                "id": m.get("id"),
                "year": (m.get("release_date") or "")[0:4]
            }
            for m in results if m.get("title") and m.get("id")
        ]
    }

def search_movies(q: str, limit: int = 5) -> list[dict]:
    """
    Search TMDB from non-router contexts for partial movie titles

    :param q: Query string.
    :type q: str
    :param limit: Maximum results to return.
    :type limit: int
    :return: List of {title, id} dicts.
    :rtype: list[dict]
    """
    params = {
        "query": q,
        "language": "en-US",
        "page": 1,
        "include_adult": False
    }
    resp = requests.get(f"{BASE_URL}/search/movie", headers=HEADERS, params=params)
    if resp.status_code != 200:
        return []
    results = resp.json().get("results", [])[:limit]
    return [
        {"title": m["title"], "id": m["id"]}
        for m in results
        if m.get("title") and m.get("id")
    ]

