from dataclasses import dataclass

@dataclass
class Livre:
    title: str
    author: str
    isbn: str

class Bibliotheque:
    def __init__(self):
        self._books = {}

    def add_book(self, livre: Livre):
        self._books[livre.isbn] = livre

    def remove_by_isbn(self, isbn: str) -> bool:
        return self._books.pop(isbn, None) is not None

    def search_by_title(self, query: str):
        q = query.lower()
        return [b for b in self._books.values() if q in b.title.lower()]

    def search_by_author(self, author: str):
        q = author.lower()
        return [b for b in self._books.values() if q in b.author.lower()]

    def count(self):
        return len(self._books)
