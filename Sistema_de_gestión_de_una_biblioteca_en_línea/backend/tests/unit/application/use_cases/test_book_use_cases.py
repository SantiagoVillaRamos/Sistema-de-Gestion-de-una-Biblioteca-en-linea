import pytest
import uuid
from domain.models.book import Book
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.use_cases.book.get_all_books_use_case import GetAllBooksUseCase
from application.dto.book_command_dto import CreateBookResult
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
async def test_add_book_successfully(use_case_dependencies, existing_author):
    
    deps = use_case_dependencies
    mock_author = deps["author_repo"]
    mock_book = deps["book_repo"]
    
    
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

    mock_book.get_all.return_value = dummy_books

    use_case = GetAllBooksUseCase(
        book_repository=mock_book,
        author_repository=mock_author
    )
    
    result_all_book = use_case.execute()
    
    
    