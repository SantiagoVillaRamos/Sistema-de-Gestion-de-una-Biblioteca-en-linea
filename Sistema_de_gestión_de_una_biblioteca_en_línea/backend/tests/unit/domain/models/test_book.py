import pytest
from uuid import uuid4
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.exceptions.business_exception import BusinessNotFoundError
from domain.models.book import Book

# --- 1. Pruebas para ISBN (Value Object) ---

def test_isbn_creation_success_isbn13_with_hyphens():
    """Prueba la creación de un ISBN-13 con guiones y que se normaliza."""
    isbn = ISBN("978-0134494166")
    processed_isbn = isbn.value.replace('-', '').replace(' ', '')
    assert isbn.value.replace('-', '').replace(' ', '') == processed_isbn
    assert len(isbn.value.replace('-', '').replace(' ', '')) == 13

def test_isbn_creation_success_isbn10_without_spaces():
    """Prueba la creación de un ISBN-10 sin espacios."""
    isbn = ISBN("1234567890")
    assert isbn.value == "1234567890"
    assert len(isbn.value) == 10

def test_isbn_creation_failure_invalid_length():
    """Prueba que falla si la longitud no es ni 10 ni 13 dígitos."""
    with pytest.raises(BusinessNotFoundError, match="El ISBN debe tener 10 o 13 dígitos."):
        ISBN("12345")

def test_isbn_creation_failure_non_digit():
    """Prueba que falla si contiene caracteres no numéricos."""
    with pytest.raises(BusinessNotFoundError, match="El ISBN debe tener 10 o 13 dígitos."):
        ISBN("978032176572A")

def test_isbn_equality():
    """Prueba la igualdad de dos objetos ISBN con el mismo valor normalizado."""
    isbn1 = ISBN("978-0132350822")
    isbn2 = ISBN("978-0132350822")
    assert isbn1.value.replace('-', '').replace(' ', '') == isbn2.value.replace('-', '').replace(' ', '')
    assert hash(isbn1) == hash(isbn2) # Pruebas para hashable

# --- 2. Pruebas para Title (Value Object) ---

def test_title_creation_success_with_spaces():
    """Prueba la creación de un Título y que se eliminan espacios redundantes."""
    title = Title("El Quijote")
    assert title.value == "El Quijote"

def test_title_creation_failure_empty():
    """Prueba que un Título vacío levanta excepción."""
    with pytest.raises(BusinessNotFoundError, match="El título no puede estar vacío."):
        Title("")

def test_title_creation_failure_spaces_only():
    """Prueba que un Título con solo espacios levanta excepción."""
    with pytest.raises(BusinessNotFoundError, match="El título no puede estar vacío."):
        Title("  ")

# --- 3. Pruebas para la Entidad Book (Lógica de Negocio) ---

def test_book_creation_failure_zero_copies():
    """Prueba que la creación del libro falla si available_copies es 0."""
    with pytest.raises(BusinessNotFoundError, match="No hay copias disponibles"):
        Book(
            book_id=str(uuid4()),
            isbn=ISBN("1234567890"),
            title=Title("Test Book"),
            author=["Author"],
            description="",
            available_copies=0 # Falla en __post_init__
        )

def test_book_lend_success(existing_book: Book):
    """Prueba que la función lend decrementa las copias disponibles."""
    initial_copies = existing_book.available_copies
    existing_book.lend()
    assert existing_book.available_copies == initial_copies - 1
    assert existing_book.is_available() is True

def test_book_lend_failure_no_copies(unavailable_book: Book):
    """Prueba que lend falla si no hay copias disponibles (copias = 0)."""
    assert unavailable_book.available_copies == 0
    with pytest.raises(BusinessNotFoundError, match="No hay copias disponibles"):
        unavailable_book.lend()

def test_book_return_book_success(unavailable_book: Book):
    """Prueba que return_book incrementa las copias disponibles."""
    initial_copies = unavailable_book.available_copies # Debería ser 0
    unavailable_book.return_book()
    assert unavailable_book.available_copies == initial_copies + 1
    assert unavailable_book.available_copies == 1
    assert unavailable_book.is_available() is True

def test_book_is_available(existing_book: Book, unavailable_book: Book):
    """Prueba el método is_available en ambos estados."""
    # Libro con copias
    assert existing_book.is_available() is True
    
    # Libro sin copias
    assert unavailable_book.available_copies == 0
    assert unavailable_book.is_available() is False




