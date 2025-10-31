from fastapi.testclient import TestClient


def test_login_successful(client: TestClient, admin_user_token):
    """Prueba de inicio de sesión exitoso."""
    
    response = admin_user_token
    assert response is not None
    assert isinstance(response, str)
    
    
    
