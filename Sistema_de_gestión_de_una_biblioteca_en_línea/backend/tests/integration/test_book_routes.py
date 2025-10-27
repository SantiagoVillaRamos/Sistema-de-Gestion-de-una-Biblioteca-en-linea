from fastapi.testclient import TestClient
from main import app

from tests.utils.auth_test_utils import create_unique_author, create_book, _extract_id, BASE_URL_BOOKS, setup_login_successful

# -----------------------------------------------
# CLIENTE Y CONFIGURACIÓN BASE
# -----------------------------------------------
client = TestClient(app)
# -----------------------------------------------
# PRUEBAS REFACTORIZADAS
# -----------------------------------------------

def test_book_creation(client, clean_db):
    """Prueba la creación de un libro usando los helpers."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    author_info = create_unique_author(client, "CleanCode Author")
    author_id = _extract_id(author_info)

    book_data = create_book(client, "Clean Code", [author_id])

    assert book_data.get("title") == "Clean Code"
    assert book_data.get("isbn") is not None
    assert book_data.get("description") == "Description for Clean Code"


def test_get_books(client, clean_db):
    """Prueba obtener todos los libros. Aseguramos que haya al menos uno."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    author_info = create_unique_author(client, "List Author")
    create_book(client, "Test Book For List", [_extract_id(author_info)])

    response = client.get(BASE_URL_BOOKS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert all("isbn" in book for book in response.json())
    assert all("title" in book for book in response.json())
    assert all("author_names" in book for book in response.json())
    assert all("description" in book for book in response.json())
    assert all("available_copies" in book for book in response.json())


def test_get_books_id(client, clean_db):
    """Prueba la obtención de un libro por su ID."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    author_info = create_unique_author(client, "Test Author ID")
    author_id = _extract_id(author_info)
    book_info = create_book(client, "Test Book", [author_id])

    # aceptar varias keys posibles para el id del libro
    book_id = book_info.get("book_id") or book_info.get("id") or book_info.get("bookId")
    assert book_id, f"No se encontró id en la respuesta: {book_info}"

    get_response = client.get(f"{BASE_URL_BOOKS}{book_id}")
    assert get_response.status_code == 200
    book_data = get_response.json()

    assert book_data.get("book_id") == book_id or book_data.get("id") == book_id
    assert book_data.get("isbn") == book_info.get("isbn")
    assert book_data.get("title") == "Test Book"
    assert book_data.get("description") == "Description for Test Book"
    assert book_data.get("available_copies") == 5
    authors = book_data.get("authors") or book_data.get("author") or []
    assert authors, "No hay autores en la respuesta"


def test_update_book(client, clean_db):
    """Prueba actualizar un libro existente."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    
    author_info = create_unique_author(client, "Update Book Author")
    author_id = _extract_id(author_info)
    book_info = create_book(client, "Book To Update", [author_id])

    book_id = book_info.get("book_id") or book_info.get("id") or book_info.get("bookId")
    assert book_id, f"No se encontró id en la respuesta: {book_info}"

    updated_data = {
        "title": "Updated Book Title",
        "description": "Updated description",
    }

    update_response = client.put(f"{BASE_URL_BOOKS}{book_id}", json=updated_data)
    assert update_response.status_code == 200
    updated_book = update_response.json()

    assert updated_book.get("title") == "Updated Book Title"
    assert updated_book.get("description") == "Updated description"
    
    response_data = update_response.json()
    assert "author_names" in response_data
    assert response_data["author_names"]
    assert "title" in response_data
    assert response_data["title"] == "Updated Book Title"
    assert "description" in response_data
    assert response_data["description"] == "Updated description"
    assert "available_copies" in response_data
    assert response_data["available_copies"] == 5 
    assert "isbn" in response_data
    assert response_data["isbn"] == book_info.get("isbn")
    
    
    
def test_delete_book(client, clean_db):
    """Prueba eliminar un libro."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    # Setup
    author_info = create_unique_author(client, "Delete Book Author")
    author_id = _extract_id(author_info)
    book_info = create_book(client, "Book To Delete", [author_id])

    book_id = book_info.get("book_id") or book_info.get("id") or book_info.get("bookId")
    assert book_id, f"No se encontró id en la respuesta: {book_info}"

    # Act - Eliminar el libro
    delete_response = client.delete(f"{BASE_URL_BOOKS}{book_id}")
    assert delete_response.status_code == 200

    response_data = delete_response.json()
    assert "message" in response_data
    assert "Libro Eliminado" in response_data["message"]
    