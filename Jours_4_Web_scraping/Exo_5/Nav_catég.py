import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

BASE_URL = "https://books.toscrape.com/"
CATEGORY_URL = BASE_URL + "catalogue/category/books/"

def get_soup(url):
    time.sleep(random.uniform(1, 2))
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    return None

def get_categories():
    soup = get_soup(BASE_URL)
    categories = {}
    for a in soup.select("div.side_categories ul li ul li a"):
        name = a.get_text(strip=True)
        href = a["href"]
        categories[name] = BASE_URL + href
    return categories

def extract_stock(text):
    try:
        return int("".join(filter(str.isdigit, text)))
    except:
        return 0

def parse_category(name, url):
    books = []
    while url:
        soup = get_soup(url)
        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = float(article.select_one(".price_color").text[1:])
            rating = article.p["class"][1]
            stock_text = article.select_one(".availability").text.strip()
            stock = extract_stock(stock_text)
            books.append({"title": title, "price": price, "rating": rating, "stock": stock})
        next_page = soup.select_one("li.next a")
        if next_page:
            url = url.rsplit("/", 1)[0] + "/" + next_page["href"]
        else:
            url = None
    return books

def compute_stats(books):
    prices = [b["price"] for b in books]
    if not prices:
        return {"count": 0, "avg": 0, "min": 0, "max": 0}
    return {
        "count": len(prices),
        "avg": round(sum(prices) / len(prices), 2),
        "min": min(prices),
        "max": max(prices)
    }

def main():
    categories = get_categories()
    summary = []
    for name, url in categories.items():
        books = parse_category(name, url)
        stats = compute_stats(books)
        stats["category"] = name
        summary.append(stats)
    df = pd.DataFrame(summary)
    df = df.sort_values(by="avg", ascending=False)
    print(df)

if __name__ == "__main__":
    main()