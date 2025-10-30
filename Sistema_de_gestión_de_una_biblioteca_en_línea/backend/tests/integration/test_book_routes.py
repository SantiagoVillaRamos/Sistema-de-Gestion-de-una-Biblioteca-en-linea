from fastapi.testclient import TestClient

from tests.utils.auth_test_utils import create_unique_author, create_book, BASE_URL_BOOKS


def test_book_creation(client: TestClient, book_prerequisites):
    """Prueba la creación de un libro usando los helpers."""
    
    book_info = book_prerequisites
    
    assert book_info["title"] == "Clean Code"
    
    assert isinstance(book_info["book_id"], str)
    assert isinstance(book_info["isbn"], str)
    assert isinstance(book_info["title"], str)
    assert isinstance(book_info["author"], list)
    assert isinstance(book_info["description"], str)
    
    assert "book_id" in book_info
    assert "isbn" in book_info
    assert "title" in book_info
    assert "author" in book_info
    assert "description" in book_info
    
    


def test_get_books(client: TestClient, admin_user_token:str):
    """Prueba obtener todos los libros. Aseguramos que haya al menos uno."""
    
    author = create_unique_author(client, token=admin_user_token)
   
    create_book(
        client, 
        token=admin_user_token,
        title="Clean Code", 
        author_ids=[author["author_id"]]
    )

    response = client.get(BASE_URL_BOOKS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert all("isbn" in book for book in response.json())
    assert all("title" in book for book in response.json())
    assert all("author_names" in book for book in response.json())
    assert all("description" in book for book in response.json())
    assert all("available_copies" in book for book in response.json())


def test_get_books_id(client: TestClient, book_prerequisites):
    """Prueba la obtención de un libro por su ID."""
    
    book_info = book_prerequisites

    book_id = book_info["book_id"]
    assert book_id, f"No se encontró id en la respuesta: {book_info}"
    
    get_response = client.get(f"{BASE_URL_BOOKS}/{book_id}")
    assert get_response.status_code == 200
    book_data = get_response.json()

    assert book_data.get("book_id") == book_id 
    assert book_data.get("isbn") == book_info.get("isbn")
    assert book_data.get("title") == "Clean Code"
    assert book_data.get("description") == "Description for Clean Code"
    assert book_data.get("available_copies") == 5
    authors = book_data.get("authors") or book_data.get("author") or []
    assert authors, "No hay autores en la respuesta"



def test_update_book(client: TestClient, admin_user_token: str, book_prerequisites):
    """Prueba actualizar un libro existente."""
    
    book_info = book_prerequisites

    book_id = book_info["book_id"]
    assert book_id, f"No se encontró id en la respuesta: {book_info}"

    updated_data = {
        "title": "Updated Book Title",
        "description": "Updated description",
    }

    update_response = client.put(
        f"{BASE_URL_BOOKS}/{book_id}", 
        json=updated_data,
        headers={"Authorization": f"Bearer {admin_user_token}"}
    )
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
    
    
    
def test_delete_book(client: TestClient, admin_user_token:str, book_prerequisites):
    """Prueba eliminar un libro."""
    
    book_info = book_prerequisites

    book_id = book_info["book_id"]
    assert book_id, f"No se encontró id en la respuesta: {book_info}"

    delete_response = client.delete(
        f"{BASE_URL_BOOKS}/{book_id}", 
        headers={"Authorization": f"Bearer {admin_user_token}"}
    )
   
    assert delete_response.status_code == 200

    response_data = delete_response.json()
    assert "message" in response_data
    assert "Libro Eliminado" in response_data["message"]
    