import pytest
from domain.models.user import User
from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.use_cases.user.get_all_users_use_case import GetAllUsersUseCase
from application.use_cases.user.get_user_use_case import GetUserUseCase
from application.dto.user_command_dto import UserDetailsDTO
import uuid



@pytest.mark.asyncio
async def test_create_user_success(create_user_command, use_case_dependencies):
    """Prueba la ejecución exitosa del caso de uso CreateUserUseCase."""

    # 1. Setup: Desempaquetar dependencias
    mock_repo = use_case_dependencies["user_repo"]
    mock_factory = use_case_dependencies["user_factory"]
    
    # 2. Crear la entidad de usuario que esperamos que devuelva el Factory
    user_id = str(uuid.uuid4())
    expected_user = User(
        user_id=user_id,
        name=create_user_command.name,
        email=create_user_command.email,
        password=create_user_command.password,
        user_type=create_user_command.user_type,
        roles=create_user_command.roles
    )

    # 3. Configurar el Mock del Factory para que devuelva la entidad esperada
    mock_factory.create.return_value = expected_user
    
    # 4. Instanciar el Caso de Uso
    use_case = CreateUserUseCase(
        user_repository=mock_repo,
        user_factory=mock_factory
    )
    
    # 5. Ejecutar (Act)
    result_user = await use_case.execute(create_user_command)
    
    # 6. Aserciones (Assert)

    # A1. Verificar que el Factory fue llamado correctamente (Lógica de creación)
    mock_factory.create.assert_called_once_with(
        name=create_user_command.name,
        email=create_user_command.email,
        password=create_user_command.password,
        user_type=create_user_command.user_type,
        roles=create_user_command.roles
    )
    
    # A2. Verificar que el Repositorio fue llamado para guardar el objeto correcto
    mock_repo.save.assert_called_once_with(expected_user)
    
    # A3. Verificar que el resultado de la ejecución sea el objeto User esperado
    assert result_user == expected_user
    assert result_user.email == create_user_command.email
    assert result_user.name == create_user_command.name
    assert result_user.password == create_user_command.password
    assert result_user.user_type == create_user_command.user_type
    assert result_user.roles == create_user_command.roles
    
    assert isinstance(result_user.name, str)
    assert isinstance(result_user.email, str)
    assert isinstance(result_user.password, str)
    assert isinstance(result_user.user_type, str)
    assert isinstance(result_user.roles, list)
    
    
@pytest.mark.asyncio
async def test_get_all_users_success(use_case_dependencies):
    
    # 1. Setup: Desempaquetar dependencias
    mock_repo = use_case_dependencies["user_repo"]
    
    dummy_users = [
        User(
            user_id=str(uuid.uuid4()), 
            name="Alice", 
            email="alice@gmail.com", 
            password="Password1234", 
            user_type="student",
            roles=["ADMIN"], 
            is_active=True
        ),
        User(
            user_id=str(uuid.uuid4()), 
            name="Bob", 
            email="bob@gmail.com", 
            password="Password12345", 
            user_type="student",
            roles=[""], 
            is_active=True
        ),
    ]
    
    # 2. Configurar el Mock: Le decimos al mock qué devolver cuando se llame a find_all
    mock_repo.find_all.return_value = dummy_users
    
    # 3. Instanciar el Caso de Uso
    use_case = GetAllUsersUseCase(user_repository=mock_repo)
    
    # 4. Ejecutar (Act)
    result_users = await use_case.execute()
    
    # 5. Aserciones (Assert)

    # A1. Verificar que el método find_all fue llamado UNA y SOLO UNA vez
    mock_repo.find_all.assert_called_once()
    
    # A2. Verificar que el resultado es exactamente el que mock_repo nos devolvió
    assert result_users == dummy_users
    assert isinstance(result_users, list)
    assert len(result_users) == 2


@pytest.mark.asyncio
async def test_get_user_with_active_loans(use_case_dependencies, existing_user, loan_and_book_data):
    """
    Prueba el flujo completo: Usuario con préstamos activos.
    Verifica que se llame a todos los repositorios y que el DTO sea correcto.
    """
    # 1. Setup: Desempaquetar dependencias y datos
    deps = use_case_dependencies
    mock_repo, mock_loan, mock_book, mock_author = deps['user_repo'], deps['loan_repo'], deps['book_repo'], deps['author_repo']
    loans, books, authors = loan_and_book_data

    book_ids = [book.book_id for book in books]
    # Mapear listas a diccionarios para la aserción final
    expected_books_map = {book.book_id: book for book in books}
    expected_authors_map = {author.author_id: author for author in authors}

    # 2. Configurar Mocks
    mock_repo.find_by_id.return_value = existing_user
    mock_loan.find_active_loans_by_user.return_value = loans
    mock_book.find_by_ids.return_value = books
    mock_author.find_by_ids.return_value = authors
    
    # 3. Instanciar el Caso de Uso
    use_case = GetUserUseCase(
        user_repo=mock_repo,
        loan_repo=mock_loan,
        book_repo=mock_book,
        author_repository=mock_author
    )
    
    # 4. Ejecutar (Act)
    result_dto = await use_case.execute(existing_user.user_id)
    
    # 5. Aserciones (Assert)
    
    # A1. Verificar el resultado principal (DTO)
    assert isinstance(result_dto, UserDetailsDTO)
    assert result_dto.user == existing_user
    assert result_dto.active_loans == loans
    assert result_dto.loaned_books_map == expected_books_map
    assert result_dto.loaned_authors_map == expected_authors_map
    
    # A2. Verificar las llamadas a los repositorios
    user_id = existing_user.user_id
    mock_repo.find_by_id.assert_called_once_with(user_id)
    mock_loan.find_active_loans_by_user.assert_called_once_with(user_id)
    mock_book.find_by_ids.assert_called_once_with(book_ids)
    mock_author.find_by_ids.assert_called_once_with(list(expected_authors_map.keys()))


@pytest.mark.asyncio
async def test_get_user_with_no_active_loans(use_case_dependencies, existing_user):
    """
    Prueba el camino corto: Usuario existe, pero no tiene préstamos activos.
    Verifica que el flujo se detenga antes de llamar a Book/Author Repositories.
    """
    # 1. Setup: Desempaquetar dependencias
    deps = use_case_dependencies
    mock_repo, mock_loan, mock_book, mock_author = deps['user_repo'], deps['loan_repo'], deps['book_repo'], deps['author_repo']

    # 2. Configurar Mocks
    mock_repo.find_by_id.return_value = existing_user
    mock_loan.find_active_loans_by_user.return_value = [] # CLAVE: Retorna lista vacía
    
    # 3. Instanciar el Caso de Uso
    use_case = GetUserUseCase(
        user_repo=mock_repo,
        loan_repo=mock_loan,
        book_repo=mock_book,
        author_repository=mock_author
    )
    
    # 4. Ejecutar (Act)
    result_dto = await use_case.execute(existing_user.user_id)
    
    # 5. Aserciones (Assert)
    
    # A1. Verificar el resultado principal (DTO)
    assert isinstance(result_dto, UserDetailsDTO)
    assert result_dto.user == existing_user
    assert result_dto.active_loans == []
    assert result_dto.loaned_books_map == {} # Debe ser mapa vacío
    assert result_dto.loaned_authors_map == {} # Debe ser mapa vacío
    
    # A2. Verificar las llamadas a los repositorios
    user_id = existing_user.user_id
    mock_repo.find_by_id.assert_called_once_with(user_id)
    mock_loan.find_active_loans_by_user.assert_called_once_with(user_id)
    
    # A3. CLAVE: Verificar que no se llamó a los repositorios de Book y Author
    mock_book.find_by_ids.assert_not_called()
    mock_author.find_by_ids.assert_not_called()