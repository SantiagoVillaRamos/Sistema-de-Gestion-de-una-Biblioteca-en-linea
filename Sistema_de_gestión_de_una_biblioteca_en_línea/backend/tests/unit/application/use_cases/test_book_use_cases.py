import pytest
import uuid
from domain.models.book import Book
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.use_cases.book.get_all_books_use_case import GetAllBooksUseCase
from application.use_cases.book.delete_book_use_case import DeleteBookUseCase
from application.use_cases.book.get_book_by_id_use_case import GetBookByIdUseCase
from application.use_cases.book.update_book_use_case import UpdateBookUseCase
from application.dto.book_command_dto import CreateBookResult,BookDetailsResponse, UpdateBookDTOCommand, UpdateBookResult
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title



@pytest.mark.asyncio
async def test_create_book_successfully(use_case_dependencies, create_book_command, existing_author):
    
    deps = use_case_dependencies
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]
    mock_factory_book = deps["book_factory"]
    
    book_id = str(uuid.uuid4())
    expected_authors = [existing_author]
    expected_author_names = [existing_author.name.value]
    
    # crea una entidad de libro que esperamos que devuelva factory
    entity_book = Book(
        book_id=book_id,
        isbn=create_book_command.isbn,
        title=create_book_command.title,
        author=create_book_command.author,
        description=create_book_command.description,
        available_copies=create_book_command.available_copies
    )
    
    # Configuración faltante: El repo de autores debe encontrar al autor
    mock_author_repo.find_by_ids.return_value = expected_authors

    mock_factory_book.create.return_value = entity_book
    
    use_case = CreateBookUseCase(
        book_repository=mock_book_repo,
        author_repository=mock_author_repo,
        book_factory=mock_factory_book
    )
    
    result_book_result = await use_case.execute(create_book_command)
    
    # Verificar que se consultó la existencia de los autores
    mock_author_repo.find_by_ids.assert_called_once_with(create_book_command.author)
    
    mock_factory_book.create.assert_called_once_with(
        isbn=create_book_command.isbn,
        title=create_book_command.title,
        author=create_book_command.author,
        description=create_book_command.description,
        available_copies=create_book_command.available_copies
    )
    
    mock_book_repo.save.assert_called_once_with(entity_book)
    
    # Verificar el resultado retornado: debe ser un CreateBookResult
    expected_result = CreateBookResult(
        book=entity_book,
        author_names=expected_author_names
    )
    
    assert result_book_result == expected_result
    assert result_book_result.book == entity_book
    assert result_book_result.author_names == expected_author_names
    


@pytest.mark.asyncio
async def test_get_all_books_successfully(use_case_dependencies, existing_author):
    
    deps = use_case_dependencies
    mock_author_repo = deps["author_repo"]
    mock_book_repo = deps["book_repo"]
    
    
    dummy_books = [
        Book(
            book_id=str(uuid.uuid4()),
            isbn=ISBN("978-0132350884"),
            title=Title("Clean Code"),
            author=[existing_author.author_id],
            description="Breve descripcion del libro Clean Code",
            available_copies=5,
        ),
        Book(
            book_id=str(uuid.uuid4()),
            isbn=ISBN("978-0132350885"),
            title=Title("Clean Arquitecture"),
            author=[existing_author.author_id],
            description="Breve descripcion del libro Clean Code",
            available_copies=6,
        )
    ]

    # El repo de libros devuelve la lista de entidades
    mock_book_repo.get_all.return_value = dummy_books

    # El repo de autores debe devolver el autor que se encuentra en los libros
    mock_author_repo.find_by_ids.return_value = [existing_author]

    # 3. Datos de Respuesta Esperados (Enriquecidos)
    expected_author_name = existing_author.name.value
    
    expected_result = [
        {
            "isbn": "978-0132350884",
            "title": "Clean Code",
            "author_names": [expected_author_name],
            "description": "Breve descripcion del libro Clean Code",
            "available_copies": 5
        },
        {
            "isbn": "978-0132350885",
            "title": "Clean Arquitecture",
            "author_names": [expected_author_name],
            "description": "Breve descripcion del libro Clean Code",
            "available_copies": 6
        }
    ]

    use_case = GetAllBooksUseCase(
        book_repository=mock_book_repo,
        author_repository=mock_author_repo
    )
    
    result_all_book = await use_case.execute()
    # A1. Verificar la llamada al repositorio de libros
    mock_book_repo.get_all.assert_called_once()
    
    # A2. Verificar la llamada al repositorio de autores
    # El set de IDs de autores únicos en los libros dummy es solo el ID del existing_author
    expected_author_ids_queried = [existing_author.author_id]
    mock_author_repo.find_by_ids.assert_called_once_with(expected_author_ids_queried)
    
    # A3. Verificar el resultado
    assert result_all_book == expected_result
    
    

@pytest.mark.asyncio
async def test_delete_book_successfully(use_case_dependencies, existing_book):
    
    deps = use_case_dependencies
    mock_book = deps["book_repo"]
    
    mock_book.find_by_id.return_value = existing_book
    
    use_case = DeleteBookUseCase(
        book_repository=mock_book
    )
    
    deleted_book = await use_case.execute(existing_book.book_id)
    
    mock_book.find_by_id.assert_called_once_with(existing_book.book_id)
    mock_book.delete.assert_called_once_with(existing_book)
    
    assert deleted_book == existing_book
    
    
    
@pytest.mark.asyncio
async def test_get_book_by_ID_successfully(use_case_dependencies, existing_book, existing_author):
    
    deps = use_case_dependencies
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]
    
    # El Use Case espera encontrar el libro
    mock_book_repo.find_by_id.return_value = existing_book
    
    # El Use Case espera encontrar los autores del libro
    mock_author_repo.find_by_ids.return_value = [existing_author]
    
    # Inicializar Use Case
    use_case = GetBookByIdUseCase(
        book_repository=mock_book_repo,
        author_repository=mock_author_repo
    )
    
    # Definir el resultado esperado
    expected_result = BookDetailsResponse(
        book=existing_book,
        authors=[existing_author]
    )
    
    # Ejecutar
    result = await use_case.execute(existing_book.book_id)
    
    # Aserciones
    
    # 1. Verificar la búsqueda del libro
    mock_book_repo.find_by_id.assert_called_once_with(existing_book.book_id)
    
    # 2. Verificar la búsqueda de autores
    # El Use Case llama find_by_ids con los IDs de autor del libro
    mock_author_repo.find_by_ids.assert_called_once_with(existing_book.author)
    
    # 3. Verificar el resultado
    assert result == expected_result



@pytest.mark.asyncio
async def test_updated_book_successfully(use_case_dependencies, existing_book, existing_author):
    
    deps = use_case_dependencies
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]

    # --- 1. Definir los datos de actualización ---
    new_title_str = "Clean Code: A Handbook of Agile Software Craftsmanship (Updated)"
    new_description = "Nueva descripcion deñ LIbro"
    
    # Crear el DTO de actualización
    update_dto = UpdateBookDTOCommand(
        title=new_title_str,
        description=new_description 
    )

    # --- 2. Configurar Mocks ---
    # El mock devuelve el libro existente (que será MUTADO in-place por el Use Case)
    mock_book_repo.find_by_id.return_value = existing_book 
    
    # El mock devuelve el autor para enriquecer el resultado
    mock_author_repo.find_by_ids.return_value = [existing_author]

    # --- 3. Definir el estado esperado del objeto Mutado para la aserción ---
    # Creamos un objeto Book para representar el estado FINAL (después de la mutación)
    expected_updated_book = Book(
        book_id=existing_book.book_id,
        isbn=existing_book.isbn,
        title=Title(new_title_str),  
        author=existing_book.author,
        description=new_description, 
        available_copies=existing_book.available_copies,
    )

    # --- 4. Inicializar y Ejecutar el Use Case ---
    use_case = UpdateBookUseCase(
        book_repository=mock_book_repo,
        author_repository=mock_author_repo
    )
    
    result: UpdateBookResult = await use_case.execute(existing_book.book_id, update_dto)

    # --- 5. Aserciones de Comportamiento (Verificar llamadas) ---
    
    # A1. Verificar que se buscó el libro
    mock_book_repo.find_by_id.assert_called_once_with(existing_book.book_id)
    
    # A2. Verificar que el método update fue llamado con el libro correctamente modificado (expected_updated_book)
    mock_book_repo.update.assert_called_once_with(expected_updated_book)
    
    # A3. Verificar que se buscaron los autores para enriquecer la respuesta
    mock_author_repo.find_by_ids.assert_called_once_with(existing_book.author)
    
    # --- 6. Aserciones de Resultado ---
    
    # A4. Verificar la respuesta final
    expected_result = UpdateBookResult(
        book=expected_updated_book,
        author_names=[existing_author.name] 
    )
    
    assert result == expected_result
    
    # A5. Verificación de Mutación (Asegura que el fixture fue modificado por el Use Case)
    assert existing_book.title == Title(new_title_str)
    assert existing_book.description == new_description
    
    

    