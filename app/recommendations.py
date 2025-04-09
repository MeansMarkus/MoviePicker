from collections import Counter
from app.tmdb_API import get_recommendations_for_movie, get_similar_movies

def get_combined_recommendations(movie_ids):
    recommended = []
    for movie_id in movie_ids:
        recs = get_recommendations_for_movie(movie_id)
        sims = get_similar_movies(movie_id)
        recommended.extend([r["id"] for r in recs + sims if "id" in r])

    count = Counter(recommended)
    sorted_recs = count.most_common()
    return [movie_id for movie_id, _ in sorted_recs]
