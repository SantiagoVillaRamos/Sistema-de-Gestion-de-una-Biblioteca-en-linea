from fastapi.testclient import TestClient
from main import app

from tests.utils.auth_test_utils import create_unique_author, _extract_id, BASE_URL_AUTHORS, setup_login_successful


# -----------------------------------------------
# CONFIGURACIÓN BASE
# -----------------------------------------------

client = TestClient(app)

# -----------------------------------------------
# PRUEBAS REFACTORIZADAS
# -----------------------------------------------
def test_author_creation(client, clean_db):
    """Prueba la creación de un autor."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    author_data = create_unique_author(client, "Test Author")
    
    assert author_data["name"].startswith("Test Author_")
    assert "description" in author_data
    assert _extract_id(author_data) is not None
    assert isinstance(author_data["author_id"], str)
    assert isinstance(author_data["description"], str)
    assert isinstance(author_data["name"], str)


def test_get_authors(client, clean_db):
    """Prueba obtener todos los autores."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    # Crear un autor para asegurar que hay datos
    create_unique_author(client, "List Author")
    
    response = client.get(BASE_URL_AUTHORS)
    assert response.status_code == 200
    
    authors = response.json()
    assert isinstance(authors, list)
    assert len(authors) > 0
    assert all("author_id" in author for author in authors)
    assert all("name" in author for author in authors)
    assert all("description" in author for author in authors)


def test_get_author_by_id(client, clean_db):
    """Prueba obtener un autor por su ID."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    # Crear autor para prueba
    author_data = create_unique_author(client, "Single Author")
    author_id = _extract_id(author_data)
    
    response = client.get(f"{BASE_URL_AUTHORS}{author_id}")
    assert response.status_code == 200
    
    retrieved_author = response.json()
    assert _extract_id(retrieved_author) == author_id
    assert retrieved_author["name"] == author_data["name"]
    assert retrieved_author["description"] == author_data["description"]
    assert "books" in retrieved_author


def test_update_author(client, clean_db):
    """Prueba actualizar un autor existente."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    # Crear autor para actualizar
    author_data = create_unique_author(client, "Update Author")
    author_id = _extract_id(author_data)
    
    # Datos actualizados
    updated_data = {
        "name": f"Updated {author_data['name']}",
        "description": "Updated description"
    }
    
    response = client.put(f"{BASE_URL_AUTHORS}{author_id}", json=updated_data)
    assert response.status_code == 200
    
    updated_author = response.json()
    assert _extract_id(updated_author) == author_id
    assert updated_author["name"] == updated_data["name"]
    assert updated_author["description"] == updated_data["description"]


def test_delete_author(client, clean_db):
    """Prueba eliminar un autor."""
    
    token = setup_login_successful(client, clean_db)
    headers = {"Authorization": f"Bearer {token}"}
    client.headers.update(headers)
    
    author_data = create_unique_author(client, "Delete Author")
    author_id = _extract_id(author_data)

    delete_response = client.delete(f"{BASE_URL_AUTHORS}{author_id}")
    assert delete_response.status_code == 200
    delete_message = delete_response.json()
    assert "message" in delete_message
    assert f"Autor eliminado, y todos sus datos han sido eliminados." in delete_message["message"]
    


