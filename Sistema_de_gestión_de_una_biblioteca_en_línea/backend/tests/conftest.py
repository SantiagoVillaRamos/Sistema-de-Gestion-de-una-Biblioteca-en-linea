import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.persistence.models import AuthorModel, BookModel, UserModel, LoanModel

from infrastructure.persistence.models import Base
from infrastructure.web.app import app
from infrastructure.persistence.repositories import SQLAlchemyAuthorRepository
from infrastructure.persistence.repositories import SQLAlchemyBookRepository
from infrastructure.persistence.repositories import SQLAlchemyUserRepository
from infrastructure.persistence.repositories import SQLAlchemyLoanRepository

# Crear base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    # Crear engine con SQLite en memoria
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    # Crear nueva sesión para cada test
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db_session):
    # Crear cliente de pruebas con dependencias
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides = {}
    return TestClient(app)

@pytest.fixture
def author_repository(db_session):
    return SQLAlchemyAuthorRepository(db_session)

@pytest.fixture
def book_repository(db_session):
    return SQLAlchemyBookRepository(db_session)

@pytest.fixture
def user_repository(db_session):
    return SQLAlchemyUserRepository(db_session)

@pytest.fixture
def loan_repository(db_session):
    return SQLAlchemyLoanRepository(db_session)

@pytest.fixture(autouse=True)
def clean_db(db_session):
    yield
    db_session.query(AuthorModel).delete()
    db_session.query(BookModel).delete()
    db_session.query(UserModel).delete()
    db_session.query(LoanModel).delete()
    db_session.commit()