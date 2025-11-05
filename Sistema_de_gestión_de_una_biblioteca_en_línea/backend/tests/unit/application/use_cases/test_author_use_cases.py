import pytest
import uuid
from application.dto.author_command_dto import CreateAuthorCommand, GetAuthorDetailsResult
from domain.models.author import Author
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription
from application.use_cases.author.create_author_use_case import CreateAuthorUseCase
from application.use_cases.author.delete_author_use_case import DeleteAuthorUseCase
from application.use_cases.author.get_all_authors_use_case import GetAllAuthorsUseCase
from application.use_cases.author.get_author_by_id_use_case import GetAuthorByIdUseCase
from application.use_cases.author.update_author_use_case import UpdateAuthorUseCase
from domain.models.exceptions.business_exception import BusinessConflictError


@pytest.mark.asyncio
async def test_create_author_successfully(use_case_dependencies):
    
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    mock_author_factory = deps["author_factory"]
    
    # 1. Datos de Entrada
    author_name = "Jane Austen"
    author_description = "Novelista inglesa, cuyas obras han sido traducidas a muchos idiomas."
    
    command = CreateAuthorCommand(
        name=author_name,
        description=author_description
    )
    
    # 2. Entidad Autor esperada (la que la fábrica debe devolver)
    # Es crucial que la entidad mockeada tenga un ID (simulando la lógica de la Factoría)
    expected_author_id = str(uuid.uuid4())
    expected_author = Author(
        author_id=expected_author_id,
        name=AuthorName(author_name),
        description=AuthorDescription(author_description)
    )
    
    # 3. Configurar Mocks
    # La factoría debe devolver el objeto Author simulado cuando se le llama
    mock_author_factory.create.return_value = expected_author
    
    # El repositorio no necesita retornar nada para el método save
    mock_author_repo.save.return_value = None

    # 4. Inicializar y Ejecutar el Use Case
    use_case = CreateAuthorUseCase(
        author_repository=mock_author_repo,
        author_factory=mock_author_factory
    )
    
    result = await use_case.execute(command)

    # 5. Aserciones de Comportamiento (Verificar llamadas)
    
    # A1. Verificar que la fábrica fue llamada con los argumentos correctos
    mock_author_factory.create.assert_called_once_with(
        name=author_name,
        description=author_description
    )
    
    # A2. Verificar que el repositorio fue llamado con la entidad Author creada
    mock_author_repo.save.assert_called_once_with(expected_author)
    
    # 6. Aserciones de Resultado
    
    # A3. Verificar que el resultado del Use Case es la entidad Author creada
    assert result == expected_author


@pytest.mark.asyncio
async def test_delete_author_successfully(use_case_dependencies, existing_author):
    
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    mock_book_repo = deps["book_repo"]
    
    author_id = existing_author.author_id
    
    # --- 1. Configurar Mocks (Camino de Éxito) ---
    
    # 1.1. El autor existe
    mock_author_repo.find_by_id.return_value = existing_author
    
    # 1.2. El autor NO tiene libros (count = 0)
    mock_book_repo.count_by_author_id.return_value = 0
    
    # 1.3. El delete no retorna nada
    mock_author_repo.delete.return_value = None

    # --- 2. Inicializar y Ejecutar el Use Case ---
    use_case = DeleteAuthorUseCase(
        author_repository=mock_author_repo,
        book_repository=mock_book_repo
    )
    
    result = await use_case.execute(author_id)
    
    # --- 3. Aserciones de Comportamiento ---
    
    # 3.1. Se buscó al autor
    mock_author_repo.find_by_id.assert_called_once_with(author_id)
    
    # 3.2. Se verificó el conteo de libros
    mock_book_repo.count_by_author_id.assert_called_once_with(author_id)
    
    # 3.3. Se llamó a delete
    mock_author_repo.delete.assert_called_once_with(author_id)
    
    # --- 4. Aserciones de Resultado ---
    assert result == existing_author
    

@pytest.mark.asyncio
async def test_delete_author_fails_if_books_associated(use_case_dependencies, existing_author):
    
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    mock_book_repo = deps["book_repo"]
    
    author_id = existing_author.author_id
    book_count = 3 # El autor tiene 3 libros
    
    # --- 1. Configurar Mocks (Camino de Fallo) ---
    
    # 1.1. El autor existe
    mock_author_repo.find_by_id.return_value = existing_author
    
    # 1.2. El autor SÍ tiene libros
    mock_book_repo.count_by_author_id.return_value = book_count

    # --- 2. Inicializar Use Case ---
    use_case = DeleteAuthorUseCase(
        author_repository=mock_author_repo,
        book_repository=mock_book_repo
    )
    
    # --- 3. Ejecutar y Verificar la Excepción ---
    # CORRECCIÓN: Reconstruir el mensaje exacto de la excepción
    author_name = existing_author.name.value
    base_message = f"El autor tiene {book_count} libros asociados y no puede ser eliminado."
    expected_error_msg = f"'{author_name}': {base_message}." # Formato inferido del error

    with pytest.raises(BusinessConflictError) as exc_info:
        await use_case.execute(author_id)
        
    # Verificar el mensaje de la excepción
    assert str(exc_info.value) == expected_error_msg
    # --- 4. Aserciones de Comportamiento (Importante) ---
    
    # 4.1. Se buscó al autor
    mock_author_repo.find_by_id.assert_called_once_with(author_id)
    
    # 4.2. Se verificó el conteo de libros
    mock_book_repo.count_by_author_id.assert_called_once_with(author_id)
    
    # 4.3. NO se llamó a delete (la lógica de negocio lo impidió)
    mock_author_repo.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_all_author_successfully(use_case_dependencies):
    
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    
    # Crear datos dummy para que el repositorio los devuelva
    author1 = Author(str(uuid.uuid4()), AuthorName("Autor 1"), AuthorDescription("Desc 1"))
    author2 = Author(str(uuid.uuid4()), AuthorName("Autor 2"), AuthorDescription("Desc 2"))
    expected_authors_list = [author1, author2]
    
    # Configurar el mock
    mock_author_repo.get_all.return_value = expected_authors_list
    
    # 2. Act (Ejecutar)
    use_case = GetAllAuthorsUseCase(author_repository=mock_author_repo)
    result = await use_case.execute()
    
    # 3. Assert (Verificar)
    
    # A1. Verificar que el resultado es el esperado
    assert result == expected_authors_list
    assert len(result) == 2
    
    # A2. Verificar que el repositorio fue llamado correctamente
    mock_author_repo.get_all.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_author_By_Id_succcessfully(
    use_case_dependencies, 
    existing_author, 
    another_author, 
    existing_books_for_author
):
    
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    mock_book_repo = deps["book_repo"]
    
    author_id_to_find = existing_author.author_id
    
    # Lista de todos los autores involucrados (principal + co-autor)
    all_authors_list = [existing_author, another_author]
    
    # El set de IDs que el Use Case debe calcular
    expected_ids_set = {existing_author.author_id, another_author.author_id}
    
    # El mapa que el Use Case debe devolver
    expected_author_map = {a.author_id: a for a in all_authors_list}

    # Configurar Mocks
    mock_author_repo.find_by_id.return_value = existing_author
    mock_book_repo.find_by_author_id.return_value = existing_books_for_author
    mock_author_repo.find_by_ids.return_value = all_authors_list
    
    # 2. Act (Ejecutar)
    use_case = GetAuthorByIdUseCase(
        author_repository=mock_author_repo,
        book_repository=mock_book_repo
    )
    result_dto = await use_case.execute(author_id_to_find)
    
    # 3. Assert (Verificar)
    
    # A1. Verificar el DTO resultante
    assert isinstance(result_dto, GetAuthorDetailsResult)
    assert result_dto.author == existing_author
    assert result_dto.books == existing_books_for_author
    assert result_dto.all_authors_map == expected_author_map
    
    # A2. Verificar las llamadas a los repositorios
    mock_author_repo.find_by_id.assert_called_once_with(author_id_to_find)
    mock_book_repo.find_by_author_id.assert_called_once_with(author_id_to_find)
    
    # A3. Verificar la llamada a find_by_ids (ignorando el orden)
    mock_author_repo.find_by_ids.assert_called_once()
    called_args_list = mock_author_repo.find_by_ids.call_args[0][0]
    assert set(called_args_list) == expected_ids_set


@pytest.mark.asyncio
async def test_update_author_successfully(
    use_case_dependencies, 
    existing_author, 
    update_author_command
):
    
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    
    command = update_author_command
    author_id = existing_author.author_id
    
    # El objeto "existing_author" será mutado por el Use Case
    
    # Configurar Mocks
    mock_author_repo.find_by_id.return_value = existing_author
    mock_author_repo.update.return_value = None # Simula el guardado
    
    # 2. Act (Ejecutar)
    use_case = UpdateAuthorUseCase(author_repository=mock_author_repo)
    result_author = await use_case.execute(author_id, command)
    
    # 3. Assert (Verificar)
    
    # A1. Verificar que el objeto devuelto (y el original) fueron mutados
    assert result_author == existing_author
    assert result_author.name == AuthorName(command.name)
    assert result_author.description == AuthorDescription(command.description)
    
    # A2. Verificar las llamadas a los mocks
    mock_author_repo.find_by_id.assert_called_once_with(author_id)
    # Verificar que "update" fue llamado con el objeto ya mutado
    mock_author_repo.update.assert_called_once_with(existing_author)
    


