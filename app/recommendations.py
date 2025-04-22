import requests
from collections import Counter
from app.movie_parser import parse_input_list
from app.tmdb_API import (
    search_movie,
    get_movie_details,
    get_recommendations_for_movie,
    get_similar_movies,
    BASE_URL,
    HEADERS,
)

def _get_keywords(self, movie_id: int) -> set[str]:
    """Get TMDB keywords for a movie"""
    url = f"{BASE_URL}/movie/{movie_id}/keywords"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return set()
    data = resp.json().get("keywords", [])
    return {kw["name"] for kw in data if "name" in kw}

def get_recommendations(self, user_inputs: list[str]) -> dict:
    #Parse each user’s lists into TMDB‐ID sets
    user_id_lists: list[set[int]] = []
    for inp in user_inputs:
        titles = parse_input_list(inp)
        ids = {
            mid
            for title in titles
            for mid in (search_movie(title),)
            if mid
        }
        user_id_lists.append(ids)

    # collect union of all input IDs
    all_input_ids = set().union(*user_id_lists)

    # find direct overlaps (only if >1 user)
    overlap_ids = (
        set.intersection(*user_id_lists)
        if len(user_id_lists) > 1
        else set()
    )

    # build overlapping movie format
    raw_overlap = [get_movie_details(mid) for mid in overlap_ids]
    overlap = [
        {
            "rating": m.get("vote_average"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
            "summary": m.get("overview"),
        }
        for m in raw_overlap
        if m
    ]

    # if there are direct overlaps, use the /recommendations endpoint
    candidates = []
    if overlap_ids:
        for mid in overlap_ids:
            candidates.extend(get_recommendations_for_movie(mid) or [])

    else:
        # if no direct overlap → fetch genres & keywords for each input movie
        genres_map   = {}
        keywords_map = {}
        for mid in all_input_ids:
            details = get_movie_details(mid) or {}
            genres_map[mid] = {g["name"] for g in details.get("genres", [])}
            keywords_map[mid] = self._get_keywords(mid)

        # for each user, collect their union of genres & keywords
        user_genre_sets = [
            set().union(*(genres_map[m] for m in uids))
            for uids in user_id_lists
        ]
        user_keyword_sets = [
            set().union(*(keywords_map[m] for m in uids))
            for uids in user_id_lists
        ]

        # compute intersection across users
        shared_genres   = set.intersection(*user_genre_sets) if len(user_genre_sets)>1 else set()
        shared_keywords = set.intersection(*user_keyword_sets) if len(user_keyword_sets)>1 else set()

        # only call /similar for movies that overlap genres or keywords with the intersection 
        for mid in all_input_ids:
            if (genres_map[mid] & shared_genres) or (keywords_map[mid] & shared_keywords):
                candidates.extend(get_similar_movies(mid) or [])

    # rank by frequency
    ids = [c["id"] for c in candidates if "id" in c]
    ranked = [mid for mid, _ in Counter(ids).most_common()]

    # exclude all original inputs
    exclude = all_input_ids.union(overlap_ids)
    recommended_ids = [mid for mid in ranked if mid not in exclude]

    # fetch top‑10
    raw_recs = [get_movie_details(mid) for mid in recommended_ids[:10]]
    recommendations = [
        {
            "rating": m.get("vote_average"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
            "summary": m.get("overview"),
        }
        for m in raw_recs
        if m
    ]

    return {
        "overlap": overlap,
        "recommendations": recommendations
    }
