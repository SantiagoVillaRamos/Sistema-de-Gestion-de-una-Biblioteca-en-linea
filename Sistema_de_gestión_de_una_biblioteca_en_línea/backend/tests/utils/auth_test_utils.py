from fastapi.testclient import TestClient
import uuid
from typing import Dict, Any, List
from main import app
import pytest

# -----------------------------------------------
# CONFIGURACIÓN BASE    
# -----------------------------------------------
BASE_URL_USERS = "/users/"
BASE_URL_LOGIN = "/auth/login"
BASE_URL_AUTHORS = "/authors/"
BASE_URL_BOOKS = "/books/"


client = TestClient(app)
# -----------------------------------------------
# FUNCIONES HELPER (PARÁ REDUCIR REPETICIÓN) USER
# -----------------------------------------------
def create_user(client, name: str, email: str, password: str, user_type: str, roles: list) -> Dict[str, Any]:
    """Crea un usuario y devuelve su respuesta JSON."""
    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "user_type": user_type,
        "roles": roles
    }
    response = client.post(BASE_URL_USERS, json=user_data)
    assert response.status_code == 201, f"Fallo al crear usuario: {response.status_code} - {response.text}"
    
    return response.json()


def login_user(client, email: str, password: str) -> str:
    
    login_response = {"email": email, "password": password}
    
    response = client.post(BASE_URL_LOGIN, json=login_response)
    assert response.status_code == 200, f"Fallo en login: {login_response.status_code} - {login_response.text}"
    return response.json()["token"]


def email_and_password_from_user_response() -> Dict[str, str]:
    
    test_email = f"admin_list_{uuid.uuid4().hex[:8]}@gmail.com"
    test_password = "AdminListPassword1234"
    
    return {
        "email": test_email,
        "password": test_password
    }



def setup_login_successful(client, clean_db):
    """Prueba de inicio de sesión exitoso."""
    
    # Primero, crear un usuario para iniciar sesión
    admin_credentials = email_and_password_from_user_response()
    create_user(
        client,
        name="Admin User",
        email=admin_credentials["email"],
        password=admin_credentials["password"],
        user_type="student",
        roles=["ADMIN"]
    )
    
    response = login_user(
        client,
        email=admin_credentials["email"],
        password=admin_credentials["password"]
    )
    assert response is not None
    assert isinstance(response, str)
    return response
    
    

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


def _extract_id(obj: Dict[str, Any]) -> str:
    return obj.get("author_id") or obj.get("id") or obj.get("authorId")  # tolerancia de keys


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

