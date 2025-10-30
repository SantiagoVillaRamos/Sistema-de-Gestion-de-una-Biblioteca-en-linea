from fastapi.testclient import TestClient
from main import app

from tests.utils.auth_test_utils import create_user, login_user, generate_unique_credentials


Client = TestClient(app)
# -----------------------------------------------
# FUNCIONES HELPER
# -----------------------------------------------

def test_login_successful(client, clean_db):
    """Prueba de inicio de sesión exitoso."""
    
    # Primero, crear un usuario para iniciar sesión
    admin_credentials = generate_unique_credentials()
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
    
    
    
