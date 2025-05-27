from typing import List, Optional, Dict

class Book:
    def __init__(self, id: int, title: str, author: str, year: int, genre: str):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

class BookService:
    def __init__(self):
        self.books: List[Book] = []
        self.next_id = 1

    def add_book(self, title: str, author: str, year: int, genre: str) -> Book:
        book = Book(self.next_id, title, author, year, genre)
        self.books.append(book)
        self.next_id += 1
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def remove_book(self, book_id: int) -> bool:
        for i, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[i]
                return True
        return False

    def search_books(self, title: Optional[str] = None, author: Optional[str] = None,
                     year: Optional[int] = None, genre: Optional[str] = None) -> List[Book]:
        results = self.books
        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if author:
            results = [book for book in results if author.lower() in book.author.lower()]
        if year:
            results = [book for book in results if book.year == year]
        if genre:
            results = [book for book in results if genre.lower() in book.genre.lower()]
        return results

    def list_books(self) -> List[Book]:
        return self.books

# Exemple d'utilisation :
# service = BookService()
# service.add_book("Le Petit Prince", "Antoine de Saint-Exupéry", 1943, "Fiction")
# books = service.search_books(author="Saint-Exupéry")