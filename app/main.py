from collections import Counter
from typing import Union, List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.filter_functions import (word_filter, content_rating_filter, audience_rating_filter)


from app.movie_parser import parse_input_list
from app.tmdb_API import (
    search_movie,
    get_movie_details,
    get_recommendations_for_movie,
    get_similar_movies,
    get_content_rating,
    get_genre_list,
    router as tmdb_router,
)

app = FastAPI()
app.include_router(tmdb_router) # Architecture: separates TMDB search endpoints from core app

@app.get("/health")
def health_check():
    """
    Health endpoint for monitoring for reliability 

    :return: Service status
    :rtype: dict
    """
    return {"status": "ok"} 

@app.get("/genres")
def fetch_genres():
    """
    Dynamically pull all genres from TMDB

    :return: List of genre names
    :rtype: dict
    """
    return {"genres": get_genre_list()}

# CORS to allow deployed frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web-production-93d43.up.railway.app"], # Security: limit which front ends can talk to api
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static") # Architecture: all client assets

# Architecture: decouples frontend from API logic
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    """
    Serve frontend page 

    :return: HTML content of frontend
    :rtype: str
    """
    with open("static/New_UI_Home.html") as f: # main UI html 
        return f.read()

# Security: ensures JSON matches expected format for input validation
class MovieListRequest(BaseModel):
    """
    Recommendations request model

    :param users: List of movie inputs
    :type users: List[Union[str, List[str]]]
    :param include: Words required in either title or summary
    :type include: List[str]
    :param exclude: Words disallowed in title or summary
    :type exclude: List[str]
    :param content_ratings: Allowed content ratings
    :type content_ratings: List[str]
    :param rating_min: Minimum TMDB audience rating allowed
    :type rating_min: float
    :param rating_max: Maximum TMDB rating allowed
    :type rating_max: float
    """
    users: List[Union[str, List[str]]]
    include:        List[str] = []
    exclude:        List[str] = []
    content_ratings:List[str] = []
    rating_min:     float     = 0.0
    rating_max:     float     = 10.0


@app.post("/recommendations")
def recommend_movies(data: MovieListRequest):
    """
    Compute overlap and movie recommendations

    :param data: Recommendation request payload
    :type data: MovieListRequest
    :return: Dict with `overlap` and filtered `recommendations` lists
    :rtype: dict
    """
    # parse each user’s input lists into sets & collect all titles
    user_lists = []
    all_titles = []
    for user_input in data.users:
        titles = parse_input_list(user_input)
        if titles:
            user_lists.append(set(titles))
            all_titles.extend(titles)

    # resolve input titles to TMDB IDs
    movie_ids = {
        mid
        for title in all_titles
        for mid in (search_movie(title),)
        if mid # drop None results
    }

    # build overlap & candidate pool
    candidates = []
    overlap = []
    overlap_ids = set()
    overlap_titles = set()

    if len(user_lists) <= 1:
        # 1 user: recommend based on all input movies
        for mid in movie_ids:
            candidates.extend(get_recommendations_for_movie(mid) or [])
    else:
        # multiple users: find titles common to all users
        overlap_titles = set.intersection(*user_lists)
        # translate overlapping titles to IDs
        overlap_ids = {
            mid
            for title in overlap_titles
            for mid in (search_movie(title),)
            if mid
        }
        # fetch overlap movie details
        raw_overlap = [get_movie_details(mid) for mid in overlap_ids]
        overlap = [ # j-son format
            {
                "rating": m.get("vote_average"),
                "title": m.get("title"),
                "content_rating": get_content_rating(m.get("id")),
                "release_date": m.get("release_date"),
                "summary": m.get("overview")
            }
            for m in raw_overlap if m
        ]

        # if there are overlapping movies, use "recommendations" endpoint
        if overlap_ids:
            for mid in overlap_ids:
                candidates.extend(get_recommendations_for_movie(mid) or [])
        else:  # No overlaps then fallback to "similar" endpoint
            for mid in movie_ids:
                candidates.extend(get_similar_movies(mid) or [])

    # DEBUG
    #print("▶ all_titles:", all_titles)
    #print("▶ movie_ids:", movie_ids)
    #print("▶ overlap_titles:", overlap_titles)
    #print("▶ overlap_ids:", overlap_ids)

    # rank by frequency
    candidate_ids = [c["id"] for c in candidates if "id" in c]
    sorted_ids = [mid for mid, _ in Counter(candidate_ids).most_common()]

    # exclude *all* input movies (and overlaps)
    exclude = movie_ids.union(overlap_ids)
    recommended_ids = [mid for mid in sorted_ids if mid not in exclude]

    # fetch top‑10 recommendation details
    raw_recs = [get_movie_details(mid) for mid in recommended_ids]
    recommendations = [
        {
            "rating": m.get("vote_average"),
            "title": m.get("title"),
            "content_rating": get_content_rating(m.get("id")),
            "release_date": m.get("release_date"),
            "summary": m.get("overview")
        }
        for m in raw_recs if m
    ]

    # apply word_filter if user provided include/exclude terms
    if data.include or data.exclude:
        recommendations = word_filter(
            recommendations,
            data.include,
            data.exclude
        )
    # apply content-rating filter if checkboxes used
    if data.content_ratings:
        recommendations = content_rating_filter(
            recommendations,
            data.content_ratings
        )
    # always apply audience-rating filter (defaults 0.0–10.0)
    recommendations = audience_rating_filter(
        recommendations,
        data.rating_min,
        data.rating_max
    )
    recommendations = recommendations[:10]
    return {
        "overlap": overlap,
        "recommendations": recommendations
    }