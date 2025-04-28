import re
import os
import requests
from bs4 import BeautifulSoup
from app.tmdb_API import _fetch_tmdb_list, BASE_URL
import json

API_KEY = os.getenv("TMDB_API_KEY") # Security: pulls api key from environment variables - secrets aren't hard coded
if not API_KEY:
    raise RuntimeError("TMDB_API_KEY environment variable is not set")

# Architecture: handles all list-parsing logic

def parse_input_list(input_data):
    """
    Accepts either a list of movie titles or URL to a movie list
    Returns list of movie titles

    :param input_data: Raw user input (list[str] or URL string)
    :type input_data: Union[list[str], str]
    :return: List of movie titles
    :rtype: list[str]
    """
    if isinstance(input_data, list):
        return input_data
    elif isinstance(input_data, str):
        input_data = input_data.strip()

        # accept manually input movies
        if '\n' in input_data or ',' in input_data:
            lines = re.split(r'\n|,', input_data)
            return [line.strip() for line in lines if line.strip()]

        # detect URL types
        if "imdb.com/list" in input_data:
            return parse_imdb_list(input_data)
        elif "letterboxd.com" in input_data:
            return parse_letterboxd_list(input_data)
        elif "themoviedb.org/list" in input_data:
            return parse_tmdb_list(input_data)
    return []


def parse_imdb_list(url):
    """
    Scrape all pages of an IMDb list and return movie titles

    :param url: URL of the IMDb list
    :type url: str
    :return: Titles from the list
    :rtype: list[str]
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    # strip off query params
    base = re.split(r'\?', url, 1)[0]
    titles = []
    next_url = base

    while next_url:
        resp = requests.get(next_url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Try JSON‑LD (new IMDb embeds whole list)
        ld = soup.find('script', {'type': 'application/ld+json'})
        if ld:
            data = json.loads(ld.string)
            if data.get('@type') == 'ItemList':
                for el in data.get('itemListElement', []):
                    name = el.get('item', {}).get('name')
                    if name:
                        titles.append(name.strip())
                # JSON‑LD covers all pages in one go
                break

        # HTML fallback - parsing list
        for div in soup.select('div.lister-item-content'):
            hdr = div.find('h3', class_='lister-item-header')
            if hdr and hdr.a and hdr.a.text:
                titles.append(hdr.a.text.strip())

        # next page link 
        nxt = soup.find('a', class_='lister-page-next')
        if nxt and nxt.get('href'):
            next_url = 'https://www.imdb.com' + nxt['href']
        else:
            break

    return titles


def parse_letterboxd_list(url: str) -> list[str]:
    """
    Scrape Letterboxd list URL for movie titles

    :param url: URL of Letterboxd list
    :type url: str
    :return: Titles from all pages
    :rtype: list[str]
    """
    titles: list[str] = []
    # Ensure URL ends with slash
    next_page = url if url.endswith('/') else url + '/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    while True:
        resp = requests.get(next_page, headers=headers)
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.content, 'lxml')
        # Poster grid for cast/crew lists, poster-list for standard lists
        container = soup.find('ul', class_='poster-list') or soup.find('div', class_='poster-grid')
        if not container:
            break
        for li in container.find_all('li'):
            img = li.find('img')
            if img and img.has_attr('alt'):
                titles.append(img['alt'].strip())
        # Next page link
        nxt = soup.find('a', class_='next')
        if not nxt or not nxt.get('href'):
            break
        next_page = BASE_URL + nxt['href']

    return titles

def parse_tmdb_list(list_url: str) -> list[str]:
    """
    Fetch TMDB list via API and return movie titles

    :param list_url: URL of TMDB list page
    :type list_url: str
    :return: Titles from TMDB list
    :rtype: list[str]
    :raises ValueError: If URL has no list ID
    """
    m = re.search(r'/list/(\d+)', list_url)
    if not m:
        raise ValueError(f"Couldn't find a list ID in {list_url}")
    list_id = m.group(1)

    resp = requests.get(
        f"{BASE_URL}/list/{list_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"language": "en‑US"}
    )
    resp.raise_for_status()
    data = resp.json()

    return [
        item.get("title", "").strip() for item in data.get("items", []) if item.get("title")
    ]
