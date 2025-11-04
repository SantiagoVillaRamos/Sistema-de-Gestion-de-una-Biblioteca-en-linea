import pytest
from domain.models.user import User
from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.use_cases.user.get_all_users_use_case import GetAllUsersUseCase
from application.use_cases.user.get_user_use_case import GetUserUseCase
from application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from application.use_cases.user.update_current_user_use_case import UpdateCurrentUserUseCase
from application.use_cases.user.get_user_loan_history_use_case import GetUserLoanHistoryUseCase
from application.dto.user_command_dto import UserDetailsDTO, UserLoanHistoryDTO
from domain.models.exceptions.business_exception import BusinessNotFoundError
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

    # Mapear listas a diccionarios para la aserción final
    expected_books_map = {book.book_id: book for book in books}
    expected_authors_map = {author.author_id: author for author in authors}

    # El conjunto esperado de IDs de autor (el orden no importa)
    expected_author_ids_set = set(expected_authors_map.keys())
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
    
    # Aserción de Book Repo: El orden de los book_ids es determinista (dado por el orden de los préstamos)
    expected_book_ids = [loans[0].book_id, loans[1].book_id]
    mock_book.find_by_ids.assert_called_once_with(expected_book_ids)
    # Aserción de Author Repo: CLAVE - Comprobamos el conjunto de IDs, ignorando el orden.
    mock_author.find_by_ids.assert_called_once()
    
    # Obtenemos el argumento real que se pasó a la llamada (que será una lista)
    actual_author_ids_list = mock_author.find_by_ids.call_args[0][0]
    
    # Comprobamos que el conjunto de IDs reales sea igual al conjunto de IDs esperados
    assert set(actual_author_ids_list) == expected_author_ids_set
    

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
    
    
@pytest.mark.asyncio
async def test_delete_user_successfully(use_case_dependencies, existing_user):
    """
    Prueba el caso de éxito: el usuario es encontrado y se llama a delete con el objeto correcto.
    """
    deps = use_case_dependencies
    mock_repo = deps["user_repo"]
    
    mock_repo.find_by_id.return_value = existing_user
    
    use_case = DeleteUserUseCase(
        user_repo=mock_repo
    )
    
    await use_case.execute(existing_user.user_id)
    
    # 1. Verificar que se llamó a find_by_id con el ID
    mock_repo.find_by_id.assert_called_once_with(existing_user.user_id)
    # 2. VERIFICACIÓN CLAVE: Verificar que se llamó a delete con el objeto User
    mock_repo.delete.assert_called_once_with(existing_user)
    
    
@pytest.mark.asyncio
async def test_delete_user_not_found(use_case_dependencies):
    """
    Prueba el caso de fallo: el usuario no se encuentra y se propaga la BusinessNotFoundError.
    """
    deps = use_case_dependencies
    mock_repo = deps["user_repo"]
    user_id_not_found = "non-existent-id"
    
    # Setup: find_by_id lanza la BusinessNotFoundError
    # Usamos side_effect en lugar de return_value para simular la excepción
    mock_repo.find_by_id.side_effect = BusinessNotFoundError(
        user_id_not_found, 
        f"Usuario con ID {user_id_not_found} no encontrado"
    )
    
    use_case = DeleteUserUseCase(
        user_repo=mock_repo
    )
    
    # Esperamos que la ejecución del Use Case lance BusinessNotFoundError
    with pytest.raises(BusinessNotFoundError):
        await use_case.execute(user_id_not_found)
        
    # 1. Verificar que se llamó a find_by_id
    mock_repo.find_by_id.assert_called_once_with(user_id_not_found)
    
    # 2. Verificar que delete NUNCA fue llamado (porque el Use Case falló antes)
    mock_repo.delete.assert_not_called()
    
    
@pytest.mark.asyncio
async def test_update_current_user_successfully(use_case_dependencies, existing_user, update_user_command):
    
    deps = use_case_dependencies
    mock_repo = deps["user_repo"]
    update_service = deps["user_updater_service"]
    
    # Objeto que el servicio devolverá (simulando la actualización)
    updated_user = User(
        user_id=existing_user.user_id,
        name=update_user_command.name,
        email=update_user_command.new_email, 
        password=update_user_command.new_password, 
        user_type=existing_user.user_type,
        roles=existing_user.roles
    )
    
    # 1. Configurar Mocks
    # CORRECCIÓN CLAVE: find_by_id debe retornar el objeto User, no solo el ID.
    mock_repo.find_by_id.return_value = existing_user
    # El servicio simula la lógica de actualización y retorna el objeto actualizado.
    update_service.update_user_data.return_value = updated_user
    
    use_case = UpdateCurrentUserUseCase(
        user_repo=mock_repo,
        user_updater_service=update_service
    )
    
    result_user = await use_case.execute(update_user_command)

    # A1. Verificar el resultado
    assert result_user == updated_user
    assert result_user.name == update_user_command.name
    assert result_user.email == update_user_command.new_email
    assert result_user.password == update_user_command.new_password
    
    assert isinstance(result_user.name, str)
    assert isinstance(result_user.email, str)
    assert isinstance(result_user.password, str)
    
    assert "Pardo Camilo" in result_user.name
    assert "Pardo_camilo@gmail.com" in result_user.email
    
    # A2. Verificar interacciones
    # Se llamó a encontrar el usuario con el ID del comando
    mock_repo.find_by_id.assert_called_once_with(update_user_command.user_id)
    
    # Se llamó al servicio de actualización con el usuario original y el comando
    update_service.update_user_data.assert_called_once_with(
        existing_user, 
        update_user_command
    )
    
    # Se llamó a guardar el usuario con el objeto *actualizado*
    mock_repo.save.assert_called_once_with(updated_user)
    
    
@pytest.mark.asyncio
async def test_update_current_user_not_found(use_case_dependencies, update_user_command):
    """
    Prueba el caso de fallo: el usuario a actualizar no se encuentra y se propaga la excepción.
    """
    deps = use_case_dependencies
    mock_repo = deps["user_repo"]
    update_service = deps["user_updater_service"]
    user_id = update_user_command.user_id
    
    # 1. Configurar Mocks: find_by_id lanza BusinessNotFoundError
    mock_repo.find_by_id.side_effect = BusinessNotFoundError(
        user_id, 
        "Usuario no encontrado"
    )
    
    use_case = UpdateCurrentUserUseCase(
        user_repo=mock_repo,
        user_updater_service=update_service
    )
    
    # Act & Assert
    with pytest.raises(BusinessNotFoundError):
        await use_case.execute(update_user_command)
        
    # Verificar interacciones
    mock_repo.find_by_id.assert_called_once_with(user_id)
    # El servicio de actualización y el repositorio.save NO deben ser llamados.
    update_service.update_user_data.assert_not_called()
    mock_repo.save.assert_not_called()
    

@pytest.mark.asyncio
async def test_get_loan_history_successfully(use_case_dependencies, existing_user, loan_history_data):
    """
    Prueba el caso de éxito: el usuario tiene historial de préstamos y la información se enriquece.
    """
    deps = use_case_dependencies
    mock_user_repo = deps["user_repo"]
    mock_loan_repo = deps["loan_repo"]
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]
    
    # Desempaquetar datos del historial
    loans, books, authors = loan_history_data
    
    # Mapeos esperados
    expected_books_map = {book.book_id: book for book in books}
    expected_authors_map = {author.author_id: author for author in authors}
    
    # IDs y conjuntos para verificación de llamadas
    expected_book_ids = [book.book_id for book in books]
    all_expected_author_ids = set()
    for book in books:
        all_expected_author_ids.update(book.author)
    
    # 1. Configurar Mocks
    mock_user_repo.find_by_id.return_value = existing_user
    # find_all_by_user devuelve la lista completa del historial
    mock_loan_repo.find_all_by_user.return_value = loans 
    mock_book_repo.find_by_ids.return_value = books
    mock_author_repo.find_by_ids.return_value = authors
    
    use_case = GetUserLoanHistoryUseCase(
        user_repo=mock_user_repo,
        loan_repo=mock_loan_repo,
        book_repo=mock_book_repo,
        author_repo=mock_author_repo
    )
    
    # Act
    result_dto = await use_case.execute(existing_user.user_id)
    
    # Assert
    # A1. Verificar el resultado y el tipo
    assert isinstance(result_dto, UserLoanHistoryDTO)
    assert result_dto.user == existing_user
    assert len(result_dto.loans) == len(loans)
    assert result_dto.loans == loans # Verifica que los préstamos sean correctos
    assert result_dto.loaned_books_map == expected_books_map
    assert result_dto.loaned_authors_map == expected_authors_map
    
    # A2. Verificar interacciones
    user_id = existing_user.user_id
    mock_user_repo.find_by_id.assert_called_once_with(user_id)
    mock_loan_repo.find_all_by_user.assert_called_once_with(user_id)
    
    # Verificar que se llamó a buscar libros con los IDs correctos (el orden no importa)
    mock_book_repo.find_by_ids.assert_called_once()
    actual_book_ids = mock_book_repo.find_by_ids.call_args[0][0]
    assert set(actual_book_ids) == set(expected_book_ids)

    # Verificar que se llamó a buscar autores con los IDs correctos (el orden no importa)
    mock_author_repo.find_by_ids.assert_called_once()
    actual_author_ids = mock_author_repo.find_by_ids.call_args[0][0]
    assert set(actual_author_ids) == all_expected_author_ids
    
    
@pytest.mark.asyncio
async def test_get_loan_history_empty(use_case_dependencies, existing_user):
    """
    Prueba el camino corto: el usuario existe pero no tiene préstamos registrados.
    """
    deps = use_case_dependencies
    mock_user_repo = deps["user_repo"]
    mock_loan_repo = deps["loan_repo"]
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]
    
    # 1. Configurar Mocks
    mock_user_repo.find_by_id.return_value = existing_user
    # find_all_by_user devuelve una lista vacía
    mock_loan_repo.find_all_by_user.return_value = [] 
    
    use_case = GetUserLoanHistoryUseCase(
        user_repo=mock_user_repo,
        loan_repo=mock_loan_repo,
        book_repo=mock_book_repo,
        author_repo=mock_author_repo
    )
    
    # Act
    result_dto = await use_case.execute(existing_user.user_id)
    
    # Assert
    assert isinstance(result_dto, UserLoanHistoryDTO)
    assert result_dto.user == existing_user
    assert result_dto.loans == []
    assert result_dto.loaned_books_map == {}
    assert result_dto.loaned_authors_map == {}
    
    # Verificar interacciones
    user_id = existing_user.user_id
    mock_user_repo.find_by_id.assert_called_once_with(user_id)
    mock_loan_repo.find_all_by_user.assert_called_once_with(user_id)
    
    # Los repositorios de Book y Author NO deben ser llamados
    mock_book_repo.find_by_ids.assert_not_called()
    mock_author_repo.find_by_ids.assert_not_called() 
    

@pytest.mark.asyncio
async def test_get_loan_history_user_not_found(use_case_dependencies):
    """
    Prueba que se lanza un error si el usuario no existe.
    """
    deps = use_case_dependencies
    mock_user_repo = deps["user_repo"]
    
    user_id_not_found = "non-existent-id"
    
    # 1. Configurar Mocks: find_by_id lanza BusinessNotFoundError
    mock_user_repo.find_by_id.side_effect = BusinessNotFoundError(
        user_id_not_found, 
        "Usuario no encontrado"
    )
    
    use_case = GetUserLoanHistoryUseCase(
        user_repo=mock_user_repo,
        loan_repo=deps["loan_repo"],
        book_repo=deps["book_repo"],
        author_repo=deps["author_repo"]
    )
    
    # Act & Assert
    with pytest.raises(BusinessNotFoundError):
        await use_case.execute(user_id_not_found)
        
    # Verificar interacciones
    mock_user_repo.find_by_id.assert_called_once_with(user_id_not_found)
    deps["loan_repo"].find_all_by_user.assert_not_called()
    deps["book_repo"].find_by_ids.assert_not_called()
    deps["author_repo"].find_by_ids.assert_not_called()
