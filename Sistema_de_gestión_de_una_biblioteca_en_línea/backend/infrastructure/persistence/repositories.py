from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

from .models import AuthorModel, BookModel, UserModel, LoanModel
from domain.models.author import Author
from domain.models.book import Book
from domain.models.user import User
from domain.models.loan import Loan
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.value_objects.due_date import DueDate
from domain.models.exceptions.business_exception import BusinessNotFoundError 

class SQLAlchemyAuthorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, author: Author) -> Author:
        db_author = AuthorModel(name=author.name)
        self.session.add(db_author)
        try:
            self.session.commit()
            self.session.refresh(db_author)
            return Author(id=db_author.id, name=db_author.name)
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, author_id: str) -> Optional[Author]:
        db_author = self.session.query(AuthorModel).filter(AuthorModel.id == int(author_id)).first()
        if not db_author:
            return None
        return Author(id=str(db_author.id), name=db_author.name)

    def get_all(self) -> List[Author]:
        db_authors = self.session.query(AuthorModel).all()
        return [Author(id=str(a.id), name=a.name) for a in db_authors]

class SQLAlchemyBookRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, book: Book) -> Book:
        db_book = BookModel(
            isbn=str(book.isbn),  
            title=str(book.title),  
            description=book.description,
            author_id=book.author[0] if book.author else None,  
            available_copies=book.available_copies
        )
        self.session.add(db_book)
        try:
            self.session.commit()
            self.session.refresh(db_book)
            return Book(
                book_id=str(db_book.id),  
                isbn=ISBN(db_book.isbn),  
                title=Title(db_book.title),  
                author=[str(db_book.author.name)] if db_book.author else [],
                description=db_book.description,
                available_copies=db_book.available_copies
            )
        except SQLAlchemyError:
            self.session.rollback()
            raise

class SQLAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        db_user = UserModel(
            name=user.name,
            email=str(user.email),
            hashed_password=str(user.password),  
            user_type=user.user_type,
            roles=",".join(user.roles), 
            is_active=user.is_active
        )
        self.session.add(db_user)
        try:
            self.session.commit()
            self.session.refresh(db_user)
            return User(
                user_id=str(db_user.id),
                name=db_user.name,
                email=Email(db_user.email),  
                password=Password(db_user.hashed_password),  
                user_type=db_user.user_type,
                roles=db_user.roles.split(",") if db_user.roles else [], 
                is_active=db_user.is_active
            )
        except SQLAlchemyError:
            self.session.rollback()
            raise

class SQLAlchemyLoanRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, loan: Loan) -> Loan:
        db_loan = LoanModel(
            user_id=int(loan.user_id),
            book_id=int(loan.book_id),
            loan_date=loan.loan_date,
            due_date=loan.due_date.value,
            is_returned=loan.is_returned
        )
        self.session.add(db_loan)
        try:
            self.session.commit()
            self.session.refresh(db_loan)
            return Loan(
                id=str(db_loan.id),
                user_id=str(db_loan.user_id),
                book_id=str(db_loan.book_id),
                loan_date=db_loan.loan_date,
                due_date=DueDate(db_loan.due_date),
                is_returned=db_loan.is_returned
            )
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, loan: Loan) -> Loan:
        db_loan = self.session.query(LoanModel).filter(LoanModel.id == int(loan.id)).first()
        if not db_loan:
            raise BusinessNotFoundError(loan.id, "Préstamo no encontrado")
        
        db_loan.is_returned = loan.is_returned
        if loan.is_returned:
            db_loan.return_date = datetime.now()
            
        try:
            self.session.commit()
            self.session.refresh(db_loan)
            return Loan(
                id=str(db_loan.id),
                user_id=str(db_loan.user_id),
                book_id=str(db_loan.book_id),
                loan_date=db_loan.loan_date,
                due_date=DueDate(db_loan.due_date),
                is_returned=db_loan.is_returned
            )
        except SQLAlchemyError:
            self.session.rollback()
            raise