import requests
from bs4 import BeautifulSoup
import time
import random
import json

SOURCES = {
    "books": "https://books.toscrape.com/catalogue/page-{}.html",
    "quotes": "http://quotes.toscrape.com/page/{}/",
    "jobs": "https://realpython.github.io/fake-jobs/"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_soup(url):
    time.sleep(random.uniform(1, 2))
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except:
        return None

def scrape_books():
    data = []
    for page in range(1, 51):
        soup = get_soup(SOURCES["books"].format(page))
        if not soup:
            break
        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = float(article.select_one(".price_color").text[1:])
            rating = article.p["class"][1]
            data.append({"source": "books", "title": title, "price": price, "rating": rating})
    return data

def scrape_quotes():
    data = []
    for page in range(1, 11):
        soup = get_soup(SOURCES["quotes"].format(page))
        if not soup:
            break
        for quote in soup.select("div.quote"):
            text = quote.select_one(".text").get_text(strip=True)
            author = quote.select_one(".author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select(".tag")]
            data.append({"source": "quotes", "text": text, "author": author, "tags": tags})
    return data

def scrape_jobs():
    data = []
    soup = get_soup(SOURCES["jobs"])
    if not soup:
        return data
    for job in soup.select("div.card-content"):
        title = job.select_one("h2.title").get_text(strip=True)
        company = job.select_one("h3.subtitle").get_text(strip=True)
        location = job.select_one("p.location").get_text(strip=True)
        data.append({"source": "jobs", "title": title, "company": company, "location": location})
    return data

def main():
    all_data = []
    all_data.extend(scrape_books())
    all_data.extend(scrape_quotes())
    all_data.extend(scrape_jobs())
    with open("multi_source_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

if __name__ == "__main__":
    main()