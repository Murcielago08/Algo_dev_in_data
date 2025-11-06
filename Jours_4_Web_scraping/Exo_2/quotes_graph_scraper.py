import requests
from bs4 import BeautifulSoup
import networkx as nx
import time
import random
from urllib.parse import urljoin

BASE_URL = "http://quotes.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def respectful_delay(min_delay=1, max_delay=2):
    time.sleep(random.uniform(min_delay, max_delay))

def extract_author_data(author_url, cache):
    """Extrait biographie, date et lieu de naissance de l’auteur (avec cache)"""
    if author_url in cache:
        return cache[author_url]
    response = requests.get(author_url, headers=HEADERS)
    if response.status_code != 200:
        return {}
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.select_one("h3.author-title").get_text(strip=True)
    birth_date = soup.select_one("span.author-born-date").get_text(strip=True)
    birth_place = soup.select_one("span.author-born-location").get_text(strip=True)
    description = soup.select_one("div.author-description").get_text(strip=True)

    cache[author_url] = {
        "name": name,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "description": description
    }
    return cache[author_url]

def scrape_quotes():
    """Scrape toutes les citations et construit un graphe Auteur–Citation–Tag"""
    G = nx.DiGraph()
    author_cache = {}
    page = 1

    while True:
        url = f"{BASE_URL}page/{page}/"
        print(f"Scraping page {page} ...")
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Fin des pages.")
            break
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.select("div.quote")
        if not quotes:
            break
        for q in quotes:
            text = q.select_one("span.text").get_text(strip=True)
            author_name = q.select_one("small.author").get_text(strip=True)
            author_link = urljoin(BASE_URL, q.select_one("a")["href"])
            tags = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]

            # Auteur
            author_data = extract_author_data(author_link, author_cache)

            G.add_node(author_name, **author_data, type="author")
            G.add_node(text, type="quote")
            G.add_edge(author_name, text, relation="wrote")

            for tag in tags:
                G.add_node(tag, type="tag")
                G.add_edge(text, tag, relation="has_tag")

            respectful_delay()

        page += 1

    nx.write_graphml(G, "quotes_graph.graphml")
    print(f"✅ Graphe exporté : quotes_graph.graphml ({len(G.nodes())} nœuds)")

if __name__ == "__main__":
    scrape_quotes()
