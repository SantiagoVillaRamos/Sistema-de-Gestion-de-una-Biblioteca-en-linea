import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Dict, Any, List
from unittest.mock import MagicMock, AsyncMock

from datetime import datetime, timedelta, timezone
from freezegun import freeze_time

from application.dto.author_command_dto import UpdateAuthorCommand
from application.dto.library_command_dto import LendBookCommand
from application.dto.book_command_dto import CreateBookCommand
from application.dto.user_command_dto import CreateUserCommand, UpdateUserCommand
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.ports.notification_service import NotificationService
from domain.models.factory.userFactory import UserFactory
from domain.models.factory.bookFactory import BookFactory
from domain.models.factory.authorFactory import AuthorFactory
from domain.models.author import Author
from domain.models.book import Book
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription
from domain.models.value_objects.due_date import DueDate

from domain.services.UpdateCurrentService import UserUpdaterService
from domain.services.lending_service import LendingService
from domain.services.returning_service import ReturningService

from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password

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

# los fixture proporcionan datos que se pueden utilizar en las pruebas.

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
    
    
#---------------------------------------------------------------------------    
    

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


#---------------------------------------------------------------------------

@pytest.fixture
def valid_email() -> Email:
    return Email(address="usuario.prueba@gmail.com")

@pytest.fixture
def valid_password() -> Password:
    return Password(hashed="random-hash-string-1234")


@pytest.fixture
def existing_user(valid_email: Email, valid_password: Password) -> User:
    """Fixture para un objeto User ya existente."""
    return User(
        user_id=str(uuid.uuid4()),
        name="Elena García",
        email=valid_email,
        password=valid_password,
        user_type="general",
        roles=["ADMIN"],
        is_active=True
    )
    

@pytest.fixture
def other_user() -> User:
    """Fixture para un objeto User ya existente."""
    return User(
        user_id=str(uuid.uuid4()),
        name="Santiago Villa",
        email="santiago.g@gmail.com",
        password="santiago_hashed_password",
        user_type="general",
        roles=[""],
        is_active=True
    )
    


@pytest.fixture
def existing_author() -> Author:
    """Fixture para un objeto User ya existente."""
    return Author(
        author_id=str(uuid.uuid4()),
        name=AuthorName("Robert C. Martin"),
        description=AuthorDescription("Este es un AUTORAZO del desarrollo de software")
    )
    

@pytest.fixture
def other_author() -> Author:
    """Fixture para un segundo autor (Co-Autor)."""
    return Author(
        author_id=str(uuid.uuid4()),
        name=AuthorName("Martin Lutero"),
        description=AuthorDescription("Escritor de la era del oscurantismo.")
    )


@pytest.fixture
def existing_book(existing_author) -> Book:
    """Fixture para un objeto User ya existente."""
    return Book(
        book_id=str(uuid.uuid4()),
        isbn=ISBN("978-0132350884"),
        title=Title("Clean Code"),
        author=[existing_author.author_id],
        description="Breve descripcion del libro Clean Code",
        available_copies=5,
    )


@pytest.fixture
def unavailable_book(other_author) -> Book:
    """Fixture para crear un libro con cero copias disponibles."""
    # Nota: para evitar que __post_init__ falle al crear 0 copias,
    # lo creamos con 1 y luego simulamos que se presta.
    book = Book(
        book_id=str(uuid.uuid4()),
        isbn=ISBN("1234567890"),
        title=Title("Last Copy"),
        author=[other_author.author_id],
        description="Breve descripcion del libro Last Copy",
        available_copies=1
    )
    book.lend() 
    return book


@pytest.fixture
def other_book(existing_author, other_author) -> Book:
    """Fixture para un objeto User ya existente."""
    return Book(
        book_id=str(uuid.uuid4()),
        isbn=ISBN("978-0132350877"),
        title=Title("Clean Arquitecture"),
        author=[existing_author.author_id, other_author.author_id],
        description="Breve descripcion del libro Clean Arquitecture",
        available_copies=5,
    )



@pytest.fixture
def expected_loan(existing_user, existing_book) -> Loan:
    """Fixture para el objeto Loan que el servicio de préstamo debe generar."""
    return Loan(
        id=str(uuid.uuid4()),
        user_id=existing_user.user_id,
        book_id=existing_book.book_id,
        loan_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14)
    )
    

@pytest.fixture
def overdue_loan(other_user, other_book) -> Loan:
    """Fixture para el objeto Loan que el servicio de préstamo debe generar."""
    return Loan(
        id=str(uuid.uuid4()),
        user_id=other_user.user_id,
        book_id=other_book.book_id,
        loan_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14)
    )
    

#---------------------------------------------------------------------------


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
    mock_notification_service = AsyncMock(spec=NotificationService)
    
    mock_lending_service = MagicMock(spec=LendingService) 
    mock_return_service = MagicMock(spec=ReturningService)
    mock_factory = MagicMock(spec=UserFactory)
    mock_factory_book = MagicMock(spec=BookFactory)
    mock_author_factory = MagicMock(spec=AuthorFactory)
    mock_update_service = MagicMock(spec=UserUpdaterService)
    
    return {
        'user_repo': mock_user_repo,
        'loan_repo': mock_loan_repo,
        'book_repo': mock_book_repo,
        'author_repo': mock_author_repo,
        'notification_service': mock_notification_service,
        'lending_service': mock_lending_service,
        'returning_service': mock_return_service,
        'user_factory': mock_factory,
        'book_factory': mock_factory_book,
        'author_factory': mock_author_factory,
        'user_updater_service': mock_update_service
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
def update_user_command(existing_user) -> UpdateUserCommand:
    """Fixture que proporciona un comando estándar para actualiazar un usuario."""

    return UpdateUserCommand(
        user_id = existing_user.user_id,
        name="Pardo Camilo",
        new_email="Pardo_camilo@gmail.com",
        new_password="securepassword123567",
        current_password=existing_user.password
    )
    
    
@pytest.fixture
def update_author_command() -> UpdateAuthorCommand:
    """Fixture que proporciona un comando estándar para actualizar un autor."""
    return UpdateAuthorCommand(
        name="Martin Fowler",
        description="Autor de Refactoring"
    )
    

@pytest.fixture
def create_book_command(existing_author) -> CreateBookCommand:
    """Fixture que proporciona un comando estándar para crear un usuario."""
    return CreateBookCommand(
        
        isbn=ISBN("978-0132350885"),
        title=Title("Clean Arquitecture"),
        author=[existing_author.author_id],
        description="Breve descripcion del libro Clean Code",
        available_copies=5,
    )


@pytest.fixture
def lend_book_command(existing_user, existing_book) -> LendBookCommand:
    """Fixture para el comando de préstamo."""
    return LendBookCommand(
        user_id=existing_user.user_id,
        book_id=existing_book.book_id
    )

    
@pytest.fixture
def active_loans() -> List[Loan]:
    """Fixture para préstamos activos del usuario (vacío para éxito)."""
    return []

    
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


@pytest.fixture
def loan_history_data(existing_user) -> tuple:
    """
    Fixture que proporciona datos complejos para el historial de préstamos: 
    Activos (sin returned_date) e Históricos (con returned_date).
    Returns: (loans_list, books_list, authors_list)
    """
    
    fixed_now = datetime.now()
    
    author_j_r_r = Author(str(uuid.uuid4()), AuthorName(value="J.R.R. Tolkien"), AuthorDescription(value="Breve descripcion del libro RAMDOM"))
    author_a_c = Author(str(uuid.uuid4()), AuthorName(value="Arthur C. Clarke"), AuthorDescription(value="Breve descripcion del libro RAMDOM"))
    authors_list = [author_j_r_r, author_a_c]
    
    book_ring = Book(str(uuid.uuid4()), ISBN(value="978-0132350884"), Title(value="The Lord of the Rings"), [author_j_r_r.author_id], "Descripcion que es RAMDOM", 5)
    book_odyssey = Book(str(uuid.uuid4()), ISBN(value="978-0132350885"), Title(value="2001: A Space Odyssey"), [author_a_c.author_id], "Descripcion que es RAMDOM", 4)
    books_list = [book_ring, book_odyssey]
    
    loan_date_1 = fixed_now - timedelta(days=20)
    due_date_1 = DueDate(fixed_now + timedelta(days=10))

    loan_date_2 = fixed_now - timedelta(days=15)
    due_date_2 = DueDate(fixed_now + timedelta(days=5))
    
    # Préstamo 1: Histórico (ya devuelto)
    loan_1 = Loan(
        id=str(uuid.uuid4()), 
        book_id=book_ring.book_id,
        user_id=existing_user.user_id,
        loan_date=loan_date_1, 
        due_date=due_date_1,
        is_returned=True
    )
    # Préstamo 2: Activo (no devuelto)
    loan_2 = Loan(
        id=str(uuid.uuid4()), 
        book_id=book_odyssey.book_id, 
        user_id=existing_user.user_id, 
        loan_date=loan_date_2, 
        due_date=due_date_2,
        is_returned=False
    )
    loans_list = [loan_1, loan_2]
    
    return loans_list, books_list, authors_list


@pytest.fixture
def existing_books_for_author(existing_author, other_author) -> List[Book]:
    """Fixture que devuelve libros escritos por el autor principal (algunos co-escritos)."""
    book1 = Book(
        book_id=str(uuid.uuid4()),
        isbn=ISBN("978-0132350884"),
        title=Title("Clean Code"),
        author=[existing_author.author_id, other_author.author_id], 
        description="...",
        available_copies=5
    )
    book2 = Book(
        book_id=str(uuid.uuid4()),
        isbn=ISBN("978-0134494166"),
        title=Title("Clean Architecture"),
        author=[existing_author.author_id], 
        description="...",
        available_copies=3
    )
    return [book1, book2]

#---------------------------------------------------------------------------

# Define una zona horaria fija para todas las pruebas
TEST_TZ = timezone(timedelta(hours=-5)) 
A_DAY = timedelta(days=1)


@pytest.fixture
def current_time():
    """Hora de referencia para simular el 'ahora'."""
    return datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ)

@pytest.fixture
def future_due_date_dt(current_time):
    """datetime en el futuro."""
    return current_time + A_DAY

@pytest.fixture
def past_due_date_dt(current_time):
    """datetime en el pasado."""
    return current_time - A_DAY

@pytest.fixture
def valid_loan_date(current_time):
    """Fecha de préstamo (un poco antes de la hora actual)."""
    return current_time - timedelta(hours=1)

# --- Fixture para un préstamo válido (usa freez_time) ---
@pytest.fixture
def valid_loan(current_time, future_due_date_dt, valid_loan_date, existing_user, existing_book) -> Loan:
    """Crea un préstamo válido."""
    with freeze_time(current_time):
        due_date = DueDate(future_due_date_dt)
        return Loan(
            id=str(uuid.uuid4()),
            book_id=existing_book.book_id,
            user_id=existing_user.user_id,
            loan_date=valid_loan_date,
            due_date=due_date,
            is_returned=False
        )


