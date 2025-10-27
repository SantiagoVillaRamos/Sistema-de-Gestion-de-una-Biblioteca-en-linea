from fastapi.testclient import TestClient
from main import app
import time
from typing import Dict, Any, List
import uuid
import pytest

# -----------------------------------------------
# CLIENTE Y CONFIGURACIÓN BASE
# -----------------------------------------------
client = TestClient(app)
BASE_URL_AUTHORS = "/authors/"
BASE_URL_BOOKS = "/books/"


def _extract_id(obj: Dict[str, Any]) -> str:
    return obj.get("author_id") or obj.get("id") or obj.get("authorId")  # tolerancia de keys


# -----------------------------------------------
# FUNCIONES HELPER (PARA REDUCIR REPETICIÓN)
# -----------------------------------------------

def create_unique_author(client, name_prefix: str = "Test Author") -> Dict[str, Any]:
    """Crea un autor único y devuelve su respuesta JSON."""
    unique_name = f"{name_prefix}_{uuid.uuid4().hex[:8]}"
    author_data = {
        "name": unique_name,
        "description": f"Description for {unique_name}"
    }
    response = client.post(BASE_URL_AUTHORS, json=author_data)
    assert response.status_code == 201, f"Fallo al crear autor: {response.status_code} - {response.text}"
    return response.json()


def create_book(client, title: str, author_ids: List[str], max_retries: int = 5) -> Dict[str, Any]:
    """Crea un libro y devuelve su respuesta JSON. Reintenta si hay conflicto por ISBN."""
    import random

    for attempt in range(max_retries):
        # Generar ISBN numérico válido de 13 dígitos (prefijo 978 + 10 dígitos aleatorios)
        unique_isbn = "978" + str(random.randint(10**9, 10**10 - 1))
        book_data = {
            "isbn": unique_isbn,
            "title": title,
            "author": author_ids,
            "description": f"Description for {title}",
            "available_copies": 5
        }
        response = client.post(BASE_URL_BOOKS, json=book_data)
        if response.status_code == 201:
            return response.json()
        if response.status_code == 409:
            # ISBN en conflicto -> reintentar con otro ISBN
            continue
        # cualquier otro status es fallo
        pytest.fail(f"Fallo inesperado al crear libro: {response.status_code} - {response.text}")
    pytest.fail(f"No se pudo crear libro tras {max_retries} intentos por conflicto de ISBN.")


# -----------------------------------------------
# PRUEBAS REFACTORIZADAS
# -----------------------------------------------

def test_book_creation(client, clean_db):
    """Prueba la creación de un libro usando los helpers."""
    author_info = create_unique_author(client, "CleanCode Author")
    author_id = _extract_id(author_info)

    book_data = create_book(client, "Clean Code", [author_id])

    assert book_data.get("title") == "Clean Code"
    assert book_data.get("isbn") is not None
    assert book_data.get("description") == "Description for Clean Code"


def test_get_books(client, clean_db):
    """Prueba obtener todos los libros. Aseguramos que haya al menos uno."""
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
    