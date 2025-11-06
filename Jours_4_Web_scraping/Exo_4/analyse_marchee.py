import requests, time
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from fpdf import FPDF

# Mapping des notes
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# Scraping des livres
def scrape_books():
    books = []
    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        res = requests.get(url)
        if res.status_code != 200:
            break
        soup = BeautifulSoup(res.content, "html.parser")
        for article in soup.select("article.product_pod"):
            title = article.h3.a["title"]
            price = float(article.select_one(".price_color").text[2:])
            rating = rating_map.get(article.p["class"][1], 0)
            stock = "In stock" in article.select_one(".instock.availability").text
            category = soup.select_one("ul.breadcrumb li:nth-of-type(2)").text.strip()
            books.append({
                "title": title, "price": price, "rating": rating,
                "stock": stock, "category": category
            })
        time.sleep(1)
    return pd.DataFrame(books)

df = scrape_books()

# Prix moyen par note
price_by_rating = df.groupby("rating")["price"].mean()

# Prix moyen par catégorie
price_by_category = df.groupby("category")["price"].mean()

# Livres en rupture de stock
out_of_stock = df[df["stock"] == False]

# Distribution des notes
rating_dist = df["rating"].value_counts()

# Corrélation note/prix
correlation = df["rating"].corr(df["price"])

# Alertes prix > 50 GBP
alerts = df[df["price"] > 50]


plt.figure(figsize=(10, 6))
sns.barplot(x=price_by_rating.index, y=price_by_rating.values)
plt.title("Prix moyen par note")
plt.xlabel("Note")
plt.ylabel("Prix moyen (£)")
plt.savefig("prix_par_note.png")

plt.figure(figsize=(12, 6))
price_by_category.sort_values().plot(kind="barh", color="skyblue")
plt.title("Prix moyen par catégorie")
plt.xlabel("Prix moyen (£)")
plt.tight_layout()
plt.savefig("prix_par_categorie.png")


pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Rapport d'analyse du marché livresque", ln=True, align="C")
pdf.cell(200, 10, txt=f"Corrélation note/prix : {correlation:.2f}", ln=True)
pdf.image("prix_par_note.png", x=10, y=30, w=180)
pdf.add_page()
pdf.image("prix_par_categorie.png", x=10, y=30, w=180)
pdf.output("rapport_livres.pdf")


fig = px.scatter(df, x="rating", y="price", color="category", hover_data=["title"])
fig.update_layout(title="Corrélation entre note et prix")
fig.show()