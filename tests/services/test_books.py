import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate

def test_create_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        isbn="1234567890",
        description="A test book"
    )

    book = service.create(obj_in=book_in)

    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"

def test_update_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Old Title",
        author="Author",
        isbn="1111111111"
    )
    book = service.create(obj_in=book_in)

    book_update = BookUpdate(title="New Title")
    updated_book = service.update(db_obj=book, obj_in=book_update)

    assert updated_book.title == "New Title"
    assert updated_book.author == "Author"

def test_get_by_isbn(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="ISBN Book",
        author="Author",
        isbn="2222222222"
    )
    book = service.create(obj_in=book_in)

    found = service.get_by_isbn(isbn="2222222222")
    assert found is not None
    assert found.id == book.id

    not_found = service.get_by_isbn(isbn="notfound")
    assert not_found is None

def test_create_book_isbn_already_used(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Duplicate",
        author="Author",
        isbn="3333333333"
    )
    service.create(obj_in=book_in)

    with pytest.raises(ValueError):
        service.create(obj_in=book_in)