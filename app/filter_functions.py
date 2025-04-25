import re
from word2number import w2n

def _normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text).lower()


def _expand_terms(terms: list[str]) -> set[str]:
    norm_set: set[str] = set()
    for term in terms:
        t = _normalize(term)
        if not t:
            continue
        norm_set.add(t)
        # try converting spelled number to numeric
        try:
            num = w2n.word_to_num(t)
            norm_set.add(str(num))
        except ValueError:
            pass
    return norm_set


def word_filter(
    recommendations: list[dict],
    include_words: list[str] = None,
    exclude_words: list[str] = None
) -> list[dict]:
    # Build normalized sets
    inc_norm = _expand_terms(include_words or [])
    exc_norm = _expand_terms(exclude_words or [])

    filtered: list[dict] = []
    for movie in recommendations:
        combined = f"{movie.get('title','')} {movie.get('summary','')}"
        text_norm = _normalize(combined)
        # include: all inc_norm must exist in text
        if inc_norm and not all(term in text_norm for term in inc_norm):
            continue
        # exclude: none of exc_norm may exist in text
        if exc_norm and any(term in text_norm for term in exc_norm):
            continue
        filtered.append(movie)
    return filtered

def content_rating_filter(
    recommendations: list[dict],
    allowed_ratings: list[str]
) -> list[dict]:
    
    if not allowed_ratings:
        return recommendations
    allowed_set = {r.strip() for r in allowed_ratings}
    return [m for m in recommendations if m.get('content_rating') in allowed_set]


def audience_rating_filter(
    recommendations: list[dict],
    min_rating: float,
    max_rating: float
) -> list[dict]:

    filtered: list[dict] = []
    for m in recommendations:
        r = m.get('rating')
        try:
            r_val = float(r)
        except (ValueError, TypeError):
            continue
        if min_rating <= r_val <= max_rating:
            filtered.append(m)
    return filtered

def genre_filter(recommendations: list[dict], allowed_genres: list[str]) -> list[dict]:
    if not allowed_genres:
        return recommendations
    allowed_set = {g.strip() for g in allowed_genres}
    filtered: list[dict] = []
    for m in recommendations:
        genres = m.get('genres', [])
        if any(g in allowed_set for g in genres):
            filtered.append(m)
    return filtered