import re
import requests
from bs4 import BeautifulSoup

def parse_input_list(input_data):
    """
    Accepts either a list of movie titles or a URL to a movie list.
    Returns a list of movie titles.
    """
    if isinstance(input_data, list):
        return input_data
    elif isinstance(input_data, str):
        input_data = input_data.strip()

        # accept manually input movies
        if '\n' in input_data or ',' in input_data:
            lines = re.split(r'\n|,', input_data)
            return [line.strip() for line in lines if line.strip()]
        
        if "imdb.com/list" in input_data:
            return parse_imdb_list(input_data)
        elif "letterboxd.com" in input_data:
            return parse_letterboxd_list(input_data)
        elif "themoviedb.org/list" in input_data:
            return parse_tmdb_list(input_data)
    return []

# ------------------ IMDb List Parsing ------------------

def parse_imdb_list(url):
    """
    Parses an IMDb list (e.g., https://www.imdb.com/list/lsXXXXXXXXXX/)
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    for div in soup.find_all("div", class_="lister-item-content"):
        header = div.find("h3", class_="lister-item-header")
        if header:
            title_tag = header.find("a")
            if title_tag:
                titles.append(title_tag.text.strip())
    return titles

# ------------------ Letterboxd List Parsing ------------------

def parse_letterboxd_list(url):
    """
    Parses a Letterboxd list (e.g., https://letterboxd.com/username/list/listname/)
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    for film_detail in soup.find_all("div", class_="film-detail-content"):
        title_tag = film_detail.find("a", class_="title")
        if title_tag:
            titles.append(title_tag.text.strip())
    if not titles:
        # Fallback for alternate layout
        for film in soup.find_all("div", class_="film-poster"):
            alt = film.get("data-film-name")
            if alt:
                titles.append(alt.strip())
    return titles

# ------------------ TMDB List Parsing (Basic) ------------------

def parse_tmdb_list(url):
    """
    Parses a TMDB list (e.g., https://www.themoviedb.org/list/123456)
    WARNING: This version scrapes HTML, since no public TMDB list API is exposed
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    for div in soup.find_all("div", class_="item"):
        title = div.find("a", class_="title")
        if title:
            titles.append(title.text.strip())
    return titles
