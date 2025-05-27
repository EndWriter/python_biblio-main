import pytest
from sqlalchemy.orm import Session

from src.models.loans import Loan
from src.models.users import User
from src.models.books import Book
from src.repositories.loans import LoanRepository
from src.services.loans import LoanService
from src.api.schemas.loans import LoanCreate, LoanUpdate

def test_create_loan(db_session: Session, user: User, book: Book):
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=user.id,
        book_id=book.id
    )
    loan = service.create(obj_in=loan_in)

    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.returned is False

def test_update_loan_returned(db_session: Session, user: User, book: Book):
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    loan = service.create(obj_in=loan_in)

    loan_update = LoanUpdate(returned=True)
    updated_loan = service.update(db_obj=loan, obj_in=loan_update)

    assert updated_loan.returned is True

def test_get_loans_by_user(db_session: Session, user: User, book: Book):
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    loan = service.create(obj_in=loan_in)

    loans = service.get_by_user(user_id=user.id)
    assert any(l.id == loan.id for l in loans)

def test_create_duplicate_loan(db_session: Session, user: User, book: Book):
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    service.create(obj_in=loan_in)

    # Suppose que le service lève une ValueError si le même livre est déjà prêté à l'utilisateur
    with pytest.raises(ValueError):
        service.create(obj_in=loan_in)