from fastapi.testclient import TestClient
from main import app


BASE_URL = "/auth/login"
BASE_URL_USERS = "/users" 
Client = TestClient(app)
# -----------------------------------------------
# FUNCIONES HELPER
# -----------------------------------------------

def test_login_successful(client, clean_db):
    """Prueba de inicio de sesión exitoso."""
    
    # Primero, crear un usuario para iniciar sesión
    user_data = {
        "name": "testuser",
        "email": "pruebas@gmail.com",
        "password": "Testpassword1234",
        "user_type": "general",
        "roles": ["USER"]
    }
    response = client.post(BASE_URL_USERS, json=user_data)
    assert response.status_code == 201, f"Fallo al crear usuario para login: {response.status_code} - {response.text}"
    # Ahora, intentar iniciar sesión con las credenciales correctas
    login_data = {
        "email": "pruebas@gmail.com",
        "password": "Testpassword1234"
    }
    response = client.post(BASE_URL, json=login_data)
    assert response.status_code == 200, f"Fallo en login: {response.status_code} - {response.text}"
    response_data = response.json()
    assert "token" in response_data
    assert response_data["token_type"] == "bearer"
    
    
          
        
