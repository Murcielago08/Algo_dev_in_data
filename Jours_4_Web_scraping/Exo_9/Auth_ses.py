import requests
from bs4 import BeautifulSoup
from time import sleep
import random

LOGIN_URL = "http://quotes.toscrape.com/login"
PROTECTED_URL = "http://quotes.toscrape.com/"
USERNAME = "admin"
PASSWORD = "admin"

def create_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    return session

def get_csrf_token(session):
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    token = soup.find("input", {"name": "csrf_token"})
    return token["value"] if token else None

def login(session):
    token = get_csrf_token(session)
    payload = {
        "csrf_token": token,
        "username": USERNAME,
        "password": PASSWORD
    }
    response = session.post(LOGIN_URL, data=payload)
    return "Logout" in response.text

def logout(session):
    session.cookies.clear()

def refresh_session(session):
    logout(session)
    sleep(random.uniform(1, 2))
    return login(session)

def access_protected(session):
    response = session.get(PROTECTED_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    quotes = soup.select("div.quote")
    return [
        {
            "text": q.select_one(".text").get_text(strip=True),
            "author": q.select_one(".author").get_text(strip=True)
        }
        for q in quotes
    ]

def main():
    session = create_session()
    if login(session):
        print("Login successful.")
        quotes = access_protected(session)
        for q in quotes:
            print(f"{q['text']} — {q['author']}")
        if not refresh_session(session):
            print("Session refresh failed.")
        else:
            print("Session refreshed.")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()