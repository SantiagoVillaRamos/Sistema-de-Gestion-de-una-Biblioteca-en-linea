from fastapi.testclient import TestClient
import uuid
import pytest
from typing import Dict, Any
from main import app
from domain.models.exceptions.business_exception import BusinessNotFoundError

# -----------------------------------------------
# CONFIGURACIÓN BASE
# -----------------------------------------------
BASE_URL = "/authors/"
client = TestClient(app)

# -----------------------------------------------
# FUNCIONES HELPER
# -----------------------------------------------
def create_unique_author(client, name_prefix: str = "Test Author") -> Dict[str, Any]:
    """Crea un autor único y devuelve su respuesta JSON."""
    unique_name = f"{name_prefix}_{uuid.uuid4().hex[:8]}"
    author_data = {
        "name": unique_name,
        "description": f"Description for {unique_name}"
    }
    response = client.post(BASE_URL, json=author_data)
    assert response.status_code == 201, f"Fallo al crear autor: {response.status_code} - {response.text}"
    return response.json()

def _extract_id(obj: Dict[str, Any]) -> str:
    """Extrae el ID de un objeto, tolerando diferentes nombres de key."""
    return obj.get("author_id") or obj.get("id") or obj.get("authorId")

# -----------------------------------------------
# PRUEBAS REFACTORIZADAS
# -----------------------------------------------
def test_author_creation(client, clean_db):
    """Prueba la creación de un autor."""
    author_data = create_unique_author(client, "Test Author")
    
    assert author_data["name"].startswith("Test Author_")
    assert "description" in author_data
    assert _extract_id(author_data) is not None
    assert isinstance(author_data["author_id"], str)
    assert isinstance(author_data["description"], str)
    assert isinstance(author_data["name"], str)


def test_get_authors(client, clean_db):
    """Prueba obtener todos los autores."""
    # Crear un autor para asegurar que hay datos
    create_unique_author(client, "List Author")
    
    response = client.get(BASE_URL)
    assert response.status_code == 200
    
    authors = response.json()
    assert isinstance(authors, list)
    assert len(authors) > 0
    assert all("author_id" in author for author in authors)
    assert all("name" in author for author in authors)
    assert all("description" in author for author in authors)


def test_get_author_by_id(client, clean_db):
    """Prueba obtener un autor por su ID."""
    # Crear autor para prueba
    author_data = create_unique_author(client, "Single Author")
    author_id = _extract_id(author_data)
    
    response = client.get(f"{BASE_URL}{author_id}")
    assert response.status_code == 200
    
    retrieved_author = response.json()
    assert _extract_id(retrieved_author) == author_id
    assert retrieved_author["name"] == author_data["name"]
    assert retrieved_author["description"] == author_data["description"]
    assert "books" in retrieved_author


def test_update_author(client, clean_db):
    """Prueba actualizar un autor existente."""
    # Crear autor para actualizar
    author_data = create_unique_author(client, "Update Author")
    author_id = _extract_id(author_data)
    
    # Datos actualizados
    updated_data = {
        "name": f"Updated {author_data['name']}",
        "description": "Updated description"
    }
    
    response = client.put(f"{BASE_URL}{author_id}", json=updated_data)
    assert response.status_code == 200
    
    updated_author = response.json()
    assert _extract_id(updated_author) == author_id
    assert updated_author["name"] == updated_data["name"]
    assert updated_author["description"] == updated_data["description"]


def test_delete_author(client, clean_db):
    """Prueba eliminar un autor."""
    
    author_data = create_unique_author(client, "Delete Author")
    author_id = _extract_id(author_data)

    delete_response = client.delete(f"{BASE_URL}{author_id}")
    assert delete_response.status_code == 200
    delete_message = delete_response.json()
    assert "message" in delete_message
    assert f"Autor eliminado, y todos sus datos han sido eliminados." in delete_message["message"]
    


