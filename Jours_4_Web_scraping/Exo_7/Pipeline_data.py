import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

BASE_URL = "https://books.toscrape.com/"
BOOKS_URL = BASE_URL + "catalogue/page-{}.html"

def get_soup(url):
    time.sleep(random.uniform(1, 2))
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    return None

def clean_price(text):
    try:
        return float(text.replace("£", "").strip())
    except:
        return None

def clean_rating(classes):
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for cls in classes:
        if cls in ratings:
            return ratings[cls]
    return None

def clean_title(text):
    return re.sub(r"\s+", " ", text.strip())

def extract_stock(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def parse_books():
    all_books = []
    for page in range(1, 51):
        soup = get_soup(BOOKS_URL.format(page))
        if not soup:
            continue
        for article in soup.select("article.product_pod"):
            title = clean_title(article.h3.a["title"])
            price = clean_price(article.select_one(".price_color").text)
            rating = clean_rating(article.p["class"])
            stock_text = article.select_one(".availability").text
            stock = extract_stock(stock_text)
            all_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "stock": stock
            })
    return all_books

def validate_data(df):
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")
    df.dropna(subset=["title", "price", "rating"], inplace=True)
    df["title"] = df["title"].apply(lambda x: x.encode("utf-8", errors="ignore").decode("utf-8"))
    return df

def detect_anomalies(df):
    anomalies = df[(df["price"] <= 0) | (df["rating"] > 5)]
    return anomalies

def main():
    books = parse_books()
    df = pd.DataFrame(books)
    df = validate_data(df)
    anomalies = detect_anomalies(df)
    print("Total books:", len(df))
    print("Anomalies detected:", len(anomalies))
    print("Sample anomalies:")
    print(anomalies.head())

if __name__ == "__main__":
    main()