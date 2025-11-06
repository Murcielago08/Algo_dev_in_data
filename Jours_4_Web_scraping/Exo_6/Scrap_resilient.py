import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import json

BASE_URL = "https://books.toscrape.com/"
PROGRESS_FILE = "progress.json"
LOG_FILE = "scraper.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def respectful_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def get_soup(session, url):
    try:
        respectful_delay()
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"page": 1, "books": []}

def parse_books(soup):
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = float(article.select_one(".price_color").text[1:])
        books.append({"title": title, "price": price})
    return books

def main():
    session = create_session()
    progress = load_progress()
    page = progress["page"]
    all_books = progress["books"]

    while True:
        url = f"{BASE_URL}catalogue/page-{page}.html" if page > 1 else f"{BASE_URL}catalogue/page-1.html"
        soup = get_soup(session, url)
        if not soup:
            break
        books = parse_books(soup)
        if not books:
            break
        all_books.extend(books)
        logging.info(f"Page {page} scraped successfully with {len(books)} books.")
        page += 1
        save_progress({"page": page, "books": all_books})

    logging.info(f"Scraping completed. Total books: {len(all_books)}")

if __name__ == "__main__":
    main()