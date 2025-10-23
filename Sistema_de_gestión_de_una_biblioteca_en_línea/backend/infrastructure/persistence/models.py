from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AuthorModel(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("BookModel", back_populates="author")

class BookModel(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)  
    author_id = Column(Integer, ForeignKey("authors.id"))
    available_copies = Column(Integer)
    author = relationship("AuthorModel", back_populates="books")
    loans = relationship("LoanModel", back_populates="book")

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    roles = Column(String)  
    is_active = Column(Boolean, default=True)
    loans = relationship("LoanModel", back_populates="user")

class LoanModel(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    loan_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)  
    is_returned = Column(Boolean, default=False)  
    return_date = Column(DateTime, nullable=True)
    user = relationship("UserModel", back_populates="loans")
    book = relationship("BookModel", back_populates="loans")