import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

jobs = soup.find_all("div", class_="card-content")
data = []

for job in jobs:
    title = job.find("h2", class_="title").get_text(strip=True)
    if "Python" not in title:
        continue

    location = job.find("p", class_="location").get_text(strip=True)
    contract_type = job.find("p", class_="is-small").get_text(strip=True)
    date_raw = job.find("time")["datetime"]
    date_clean = pd.to_datetime(date_raw).strftime("%Y-%m-%d")

    apply_link = job.find("a", string=re.compile("Apply"))["href"]
    apply_link_valid = apply_link.startswith("https://")

    data.append({
        "title": title,
        "location": location,
        "contract": contract_type,
        "date": date_clean,
        "apply_url": apply_link if apply_link_valid else "Invalid URL"
    })

df = pd.DataFrame(data)
df.drop_duplicates(inplace=True)
df.to_csv("filtered_jobs.csv", index=False, encoding="utf-8")

# Statistiques
print(df["location"].value_counts())
print(df["contract"].value_counts())