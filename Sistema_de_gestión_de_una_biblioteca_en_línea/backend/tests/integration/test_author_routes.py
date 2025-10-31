from fastapi.testclient import TestClient
import uuid
from tests.utils.auth_test_utils import _extract_id, BASE_URL_AUTHORS



def test_author_creation(client: TestClient, author_prerequisites):
    """Prueba la creación de un autor."""
    
    author_data = author_prerequisites
    
    assert author_data["name"].startswith("Autor")
    assert "description" in author_data
    assert _extract_id(author_data) is not None
    assert isinstance(author_data["author_id"], str)
    assert isinstance(author_data["description"], str)
    assert isinstance(author_data["name"], str)


def test_get_authors(client: TestClient, admin_user_token:str, author_prerequisites):
    """Prueba obtener todos los autores."""
    
    author_data = author_prerequisites
    
    headers = {"Authorization": f"Bearer {admin_user_token}"}
    
    response = client.get(BASE_URL_AUTHORS, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("author_id" in author for author in data)
    assert all("name" in author for author in data)
    assert all("description" in author for author in data)
    assert any(author["author_id"] == author_data["author_id"] for author in data)


def test_get_author_by_id(client: TestClient, author_prerequisites):
    """Prueba obtener un autor por su ID."""
    
    author_data = author_prerequisites
    
    author_id = author_data["author_id"] 
    assert author_id is not None, "Error de Depuración: El diccionario de autor no contiene 'id' ni 'author_id'."
    
    url = f"{BASE_URL_AUTHORS}{author_id}"
    response = client.get(url)
    
    assert response.status_code == 200, f"Fallo {response.status_code} - {response.text}"
    
    retrieved_author = response.json()
    assert retrieved_author["name"] == author_data["name"]
    assert retrieved_author["description"] == author_data["description"]
    assert "books" in retrieved_author


def test_update_author(client: TestClient, admin_user_token:str, author_prerequisites):
    """Prueba actualizar un autor existente."""
    
    author_data = author_prerequisites
    author_id = author_data["author_id"]
    
    headers = {"Authorization": f"Bearer {admin_user_token}"}
    url = f"{BASE_URL_AUTHORS}{author_id}"

    response = client.put(url, json=author_data, headers=headers)
    assert response.status_code == 200
    
    updated_author = response.json()
    assert _extract_id(updated_author) == author_id
    assert updated_author["name"] == author_data["name"]
    assert updated_author["description"] == author_data["description"]



def test_delete_author(client: TestClient, admin_user_token:str, author_prerequisites):
    """Prueba eliminar un autor."""
    
    author_data = author_prerequisites
    author_id = author_data["author_id"]
    
    headers = {"Authorization": f"Bearer {admin_user_token}"}
    url = f"{BASE_URL_AUTHORS}{author_id}"

    # Eliminación exitosa
    response = client.delete(url, headers=headers)
    assert response.status_code == 200
    
    response_check = client.get(url, headers=headers)
    assert response_check.status_code == 404
    
    delete_message = response.json()
    assert "message" in delete_message
    assert f"Autor eliminado, y todos sus datos han sido eliminados." in delete_message["message"]
    


