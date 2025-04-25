from collections import Counter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List
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
app.include_router(tmdb_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/genres")
def fetch_genres():
    #Fetch and return TMDB genres dynamically
    return {"genres": get_genre_list()}


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
    users: List[Union[str, List[str]]]
    include:        List[str] = []
    exclude:        List[str] = []
    content_ratings:List[str] = []
    rating_min:     float     = 0.0
    rating_max:     float     = 10.0


@app.post("/recommendations")
def recommend_movies(data: MovieListRequest):
    # Parse each user’s list into sets & collect all titles
    user_lists = []
    all_titles = []
    for user_input in data.users:
        titles = parse_input_list(user_input)
        if titles:
            user_lists.append(set(titles))
            all_titles.extend(titles)

    # Resolve all input titles to TMDB IDs
    movie_ids = {
        mid
        for title in all_titles
        for mid in (search_movie(title),)
        if mid
    }

    # Build overlap & candidate pool
    candidates = []
    overlap = []
    overlap_ids = set()
    overlap_titles = set()

    if len(user_lists) <= 1:
        for mid in movie_ids:
            candidates.extend(get_recommendations_for_movie(mid) or [])
    else:
        overlap_titles = set.intersection(*user_lists)
        overlap_ids = {
            mid
            for title in overlap_titles
            for mid in (search_movie(title),)
            if mid
        }
        # Fetch overlap details
        raw_overlap = [get_movie_details(mid) for mid in overlap_ids]
        overlap = [
            {
                "rating": m.get("vote_average"),
                "title": m.get("title"),
                "content_rating": get_content_rating(m.get("id")),
                "release_date": m.get("release_date"),
                "summary": m.get("overview")
            }
            for m in raw_overlap if m
        ]

        # Recommendations from overlaps
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

    # Rank by frequency
    candidate_ids = [c["id"] for c in candidates if "id" in c]
    sorted_ids = [mid for mid, _ in Counter(candidate_ids).most_common()]

    # Exclude *all* input movies (and overlaps)
    exclude = movie_ids.union(overlap_ids)
    recommended_ids = [mid for mid in sorted_ids if mid not in exclude]

    # Fetch top‑10 recommendation details
    raw_recs = [get_movie_details(mid) for mid in recommended_ids[:10]]
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
        recommendations = word_filter(recommendations, data.include, data.exclude)
        recommendations = content_rating_filter(recommendations, data.content_ratings)
        recommendations = audience_rating_filter(recommendations, data.rating_min, data.rating_max)
    return {
        "overlap": overlap,
        "recommendations": recommendations
    }

def search_movies_endpoint(q: str):
    return {"results": search_movies(q)}
