import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Dict, Any, List
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timedelta

from application.dto.user_command_dto import CreateUserCommand
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from domain.models.factory.userFactory import UserFactory
from domain.models.author import Author
from domain.models.book import Book
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription
from domain.models.value_objects.due_date import DueDate

from infrastructure.persistence.models import AuthorModel, BookModel, UserModel, LoanModel

from infrastructure.persistence.models import Base
from main import app
from infrastructure.persistence.repositories import SQLAlchemyAuthorRepository
from infrastructure.persistence.repositories import SQLAlchemyBookRepository
from infrastructure.persistence.repositories import SQLAlchemyUserRepository
from infrastructure.persistence.repositories import SQLAlchemyLoanRepository
from infrastructure.persistence.database import get_db

from tests.utils.auth_test_utils import create_book, create_user, generate_unique_credentials, login_user, create_unique_author

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
    
    app.dependency_overrides[get_db] = override_get_db
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
    

@pytest.fixture(scope="function")
def admin_credentials_data() -> Dict[str, str]:
    """Genera credenciales únicas (Email/Password) para cada prueba."""
    
    return generate_unique_credentials()


@pytest.fixture(scope="function")
def borrower_credentials_data() -> Dict[str, str]:
    """Genera credenciales únicas para el usuario Prestatario."""
    # Esto asegura que Admin y Borrower usen emails diferentes para un mismo test.
    return generate_unique_credentials()


@pytest.fixture(scope="function")
def admin_user_token(client: TestClient, admin_credentials_data: Dict[str, str]) -> str:
    """
    Crea un usuario administrador, hace login y devuelve su token JWT.
    Scope 'function' para evitar ScopeMismatch con el fixture 'client'.
    """
    
    # 1. Crear el usuario con rol ADMINISTRADOR
    create_user(
        client,
        name="Global Admin",
        password=admin_credentials_data["password"],
        user_type="general",
        roles=["ADMIN"],
        email=admin_credentials_data["email"]
    )
    
    # 2. Iniciar sesión y obtener el token
    return login_user(client, admin_credentials_data["email"], admin_credentials_data["password"])


    
@pytest.fixture(scope="function")
def loan_prerequisites(client: TestClient, borrower_credentials_data: Dict[str, str], admin_user_token: str) -> Dict[str, Any]:
    """
    Fixture que realiza el setup completo para un préstamo:
    1. Crea un usuario (el prestatario, 'student').
    2. Crea un autor y un libro.
    3. Devuelve el ID del usuario, el ID del libro y el token del prestatario.
    """
    
    author = create_unique_author(client, token=admin_user_token)
   
    book = create_book(
        client, 
        token=admin_user_token,
        title="Libro de Préstamo", 
        author_ids=[author["author_id"]]
    )
    
    user_credentials = borrower_credentials_data
    
    borrower_user = create_user(
        client,
        name="Borrower User",
        email=user_credentials["email"],
        password=user_credentials["password"],
        user_type="student",
        roles=["ADMIN"]
    )
    borrower_token = login_user(client, user_credentials["email"], user_credentials["password"])
    
    # 3. Retornar los datos esenciales para la prueba de préstamo
    return {
        "borrower_id": borrower_user["user_id"],
        "borrower_token": borrower_token,
        "book_id": book["book_id"],
        "book_isbn": book["isbn"]
    }


@pytest.fixture(scope="function")
def book_prerequisites(client: TestClient, admin_user_token: str):
    
    author = create_unique_author(client, token=admin_user_token)
   
    book_info = create_book(
        client, 
        token=admin_user_token,
        title="Clean Code", 
        author_ids=[author["author_id"]]
    )
    return book_info
    

@pytest.fixture(scope="function")
def author_prerequisites(client: TestClient, admin_user_token: str):
    
    author_data = create_unique_author(
        client, 
        token=admin_user_token,
        name_prefix="Autor para una lista de pruebas"
    )
    return author_data


@pytest.fixture(scope="function")
def create_user_prerequisites(client: TestClient):
    
    test_data = generate_unique_credentials()
    
    user_data = create_user(
        client,
        name="Test User",
        email=test_data["email"],
        password=test_data["password"],
        user_type="general",
        roles=["student"]
    )
    return user_data, test_data


@pytest.fixture
def existing_user() -> User:
    """Fixture para un objeto User ya existente."""
    return User(
        user_id=str(uuid.uuid4()),
        name="Elena García",
        email="elena.g@gmail.com",
        password="hashed_password",
        user_type="general",
        roles=["ADMIN"],
        is_active=True
    )


@pytest.fixture
def use_case_dependencies():
    """
    Fixture que proporciona mocks de las dependencias.
    Devuelve una tupla (mock_repo, mock_factory).
    """
    mock_user_repo = AsyncMock(spec=UserRepository)
    mock_loan_repo = AsyncMock(spec=LoanRepository)
    mock_book_repo = AsyncMock(spec=BookRepository)
    mock_author_repo = AsyncMock(spec=AuthorRepository)
    mock_factory = MagicMock(spec=UserFactory)
    
    return {
        'user_repo': mock_user_repo,
        'loan_repo': mock_loan_repo,
        'book_repo': mock_book_repo,
        'author_repo': mock_author_repo,
        'user_factory': mock_factory
    }



@pytest.fixture
def create_user_command() -> CreateUserCommand:
    """Fixture que proporciona un comando estándar para crear un usuario."""
    return CreateUserCommand(
        name="John Doe",
        email="john.doe@gmail.com",
        password="securepassword123",
        user_type="general",
        roles=["ADMIN"],
    )
    
    
@pytest.fixture
def loan_and_book_data(existing_user) -> tuple:
    """
    Fixture que proporciona datos complejos de préstamos, libros y autores
    para simular el flujo completo.
    Returns: (loans_list, books_list, authors_list)
    """
    # Autores
    author_j_r_r = Author(str(uuid.uuid4()), AuthorName(value="J.R.R. Tolkien"), AuthorDescription(value="Breve descripcion del libro RAMDOM"))
    author_a_c = Author(str(uuid.uuid4()), AuthorName(value="Arthur C. Clarke"), AuthorDescription(value="Breve descripcion del libro RAMDOM"))
    authors_list = [author_j_r_r, author_a_c]
    
    # Libros
    book_ring = Book(str(uuid.uuid4()), ISBN(value="978-0132350884"), Title(value="The Lord of the Rings"), [author_j_r_r.author_id], "Descripcion que es RAMDOM", 5)
    book_odyssey = Book(str(uuid.uuid4()), ISBN(value="978-0132350885"), Title(value="2001: A Space Odyssey"), [author_a_c.author_id], "Descripcion que es RAMDOM", 4)
    books_list = [book_ring, book_odyssey]
    
    # CLAVE: Definir instancias de datetime y DueDate
    loan_date_1 = datetime.now() - timedelta(days=5)
    due_date_1 = DueDate(loan_date_1 + timedelta(days=10))

    loan_date_2 = datetime.now() - timedelta(days=1)
    due_date_2 = DueDate(loan_date_2 + timedelta(days=14))
    
    # Préstamos Activos
    loan_1 = Loan(str(uuid.uuid4()), book_ring.book_id, existing_user.user_id, loan_date=loan_date_1, due_date=due_date_1)
    loan_2 = Loan(str(uuid.uuid4()), book_odyssey.book_id, existing_user.user_id, loan_date=loan_date_2, due_date=due_date_2)
    loans_list = [loan_1, loan_2]
    
    return loans_list, books_list, authors_list