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
    allowed_bins: list[int]
) -> list[dict]:
    if not allowed_bins:
        return recommendations
    filtered: list[dict] = []
    for m in recommendations:
        rating = m.get('rating')
        if rating is None:
            continue
        try:
            bin_index = int(rating)
        except (ValueError, TypeError):
            continue
        if bin_index in allowed_bins:
            filtered.append(m)
    return filtered