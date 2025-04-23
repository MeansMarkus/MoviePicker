from collections import Counter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.filter_functions import word_filter

from app.movie_parser import parse_input_list
from app.tmdb_API import (
    search_movie,
    get_movie_details,
    get_recommendations_for_movie,
    get_similar_movies
)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web-production-93d43.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("static/index.html") as f:
        return f.read()

class MovieListRequest(BaseModel):
    users: list[str]
    include: list[str] = []  
    exclude: list[str] = []  

@app.post("/recommendations")
def recommend_movies(data: MovieListRequest):
    # 1) Parse each user’s list into sets & collect all titles
    user_lists = []
    all_titles = []
    for user_input in data.users:
        titles = parse_input_list(user_input)
        user_lists.append(set(titles))
        all_titles.extend(titles)

    # 2) Determine overlap titles (only if >1 user)
    overlap_titles = set.intersection(*user_lists) if len(user_lists) > 1 else set()

    # 3) Resolve all input titles to TMDB IDs
    movie_ids = {
        mid
        for title in all_titles
        for mid in [search_movie(title)]
        if mid
    }

    # 4) Resolve overlap titles to TMDB IDs
    overlap_ids = {
        mid
        for title in overlap_titles
        for mid in [search_movie(title)]
        if mid
    }

    # 5) Fetch overlap movie details
    raw_overlap = [get_movie_details(mid) for mid in overlap_ids]
    overlap = [
        {
            "rating": m.get("vote_average"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
            "summary": m.get("overview")
        }
        for m in raw_overlap if m
    ]

    # 6) Build candidate pool
    candidates = []
    if overlap_ids:
        # a) If there are overlaps, use the “recommendations” endpoint
        for mid in overlap_ids:
            candidates.extend(get_recommendations_for_movie(mid) or [])
    else:
        # b) Otherwise, fall back to the “similar” endpoint
        for mid in movie_ids:
            candidates.extend(get_similar_movies(mid) or [])

    # 7) Rank by frequency
    candidate_ids = [c["id"] for c in candidates if "id" in c]
    sorted_ids = [mid for mid, _ in Counter(candidate_ids).most_common()]

    # 8) Exclude *all* input movies (and overlaps)
    exclude = movie_ids.union(overlap_ids)
    recommended_ids = [mid for mid in sorted_ids if mid not in exclude]

    # 9) Fetch top‑10 recommendation details
    raw_recs = [get_movie_details(mid) for mid in recommended_ids[:10]]
    recommendations = [
        {
            "rating": m.get("vote_average"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
            "summary": m.get("overview")
        }
        for m in raw_recs if m
    ]

    # apply word_filter if user provided include/exclude terms
    if data.include or data.exclude:
        recommendations = word_filter(recommendations, data.include, data.exclude)

    return {
        "overlap": overlap,
        "recommendations": recommendations
    }