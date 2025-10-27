from fastapi.testclient import TestClient
from main import app

from tests.utils.auth_test_utils import create_user, login_user, email_and_password_from_user_response, setup_login_successful


# -----------------------------------------------
# CONFIGURACIÓN BASE    
# -----------------------------------------------
BASE_URL = "/users/"
client = TestClient(app)
# -----------------------------------------------

# -----------------------------------------------
# PRUEBAS       
# -----------------------------------------------
def test_create_user(client, clean_db):
    """Prueba la creación de un usuario."""
    
    test_data = email_and_password_from_user_response()
    
    user_data = create_user(
        client,
        name="Test User",
        email=test_data["email"],
        password=test_data["password"],
        user_type="general",
        roles=["student"]
    )
    
    assert user_data["name"] == "Test User"
    assert user_data["email"] == test_data["email"]
    assert user_data["user_type"] == "general"
    assert user_data["roles"] == ["student"]
    
    assert "email" in user_data
    assert "user_id" in user_data
    assert "name" in user_data
    assert "user_type" in user_data
    assert "roles" in user_data
    assert "password" not in user_data # Asegurarse de que la contraseña no se devuelve
    
    assert isinstance(user_data["user_id"], str)
    assert isinstance(user_data["name"], str)
    assert isinstance(user_data["email"], str)
    assert isinstance(user_data["user_type"], str)
    assert isinstance(user_data["roles"], list)



def test_get_users(client, clean_db):
    """Prueba obtener todos los usuarios."""

    token = setup_login_successful(client, clean_db)
    response = client.get(BASE_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Fallo al obtener usuarios: {response.status_code} - {response.text}"
    
    reponse_data = response.json()
    users = reponse_data.get("users") or reponse_data.get("Users") or []
    
    assert users is not None, "No se encontraron usuarios en la respuesta"
    assert isinstance(users, list)
    
    assert "users" in reponse_data
    assert isinstance(reponse_data["users"], list)
    
    assert len(users) > 0
    assert all("user_id" in user for user in users)
    assert all("name" in user for user in users)
    assert all("email" in user for user in users)
    assert all("user_type" in user for user in users)
    assert all("roles" in user for user in users)
    assert all("is_active" in user for user in users)
    
    assert all(isinstance(user["user_id"], str) for user in users)
    assert all(isinstance(user["name"], str) for user in users)
    assert all(isinstance(user["email"], str) for user in users)
    assert all(isinstance(user["user_type"], str) for user in users)
    assert all(isinstance(user["roles"], list) for user in users)
    assert all(isinstance(user["is_active"], bool) for user in users)
    
    # valida que ADMIN este en roles de al menos un usuario
    assert any("ADMIN" in user["roles"] for user in users)
    
    
    
def test_get_user_by_id(client, clean_db):
    """Prueba obtener un usuario por su ID."""
    
    test_data = email_and_password_from_user_response()

    user_data = create_user(
        client,
        name="Single User",
        email=test_data["email"],
        password=test_data["password"],
        user_type="general",
        roles=["student"]
    )
    user_id = user_data["user_id"]
    token = login_user(client, test_data["email"], test_data["password"])
    response = client.get(f"{BASE_URL}{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, f"Fallo al obtener usuarios: {response.status_code} - {response.text}"
    
    retrieved_user = response.json()
    
    assert retrieved_user["user_id"] == user_id
    assert retrieved_user["name"] == user_data["name"]
    assert retrieved_user["email"] == user_data["email"]
    assert retrieved_user["is_active"] == True
    
    assert "password" not in retrieved_user
    assert "loaned_books" in retrieved_user
    assert "email" in retrieved_user
    assert "user_id" in retrieved_user
    assert "name" in retrieved_user
    assert "is_active" in retrieved_user
    
    assert isinstance(retrieved_user["user_id"], str)
    assert isinstance(retrieved_user["name"], str)
    assert isinstance(retrieved_user["email"], str)
    assert isinstance(retrieved_user["is_active"], bool)
    assert isinstance(retrieved_user["loaned_books"], list)
    
    assert all("loan_id" in book for book in retrieved_user["loaned_books"])
    assert all("book_title" in book for book in retrieved_user["loaned_books"])
    assert all("description" in book for book in retrieved_user["loaned_books"])
    assert all("authors" in book for book in retrieved_user["loaned_books"])
    assert all("loan_date" in book for book in retrieved_user["loaned_books"])
    assert all("due_date" in book for book in retrieved_user["loaned_books"])
    
    assert all(isinstance(book["loan_id"], str) for book in retrieved_user["loaned_books"])
    assert all(isinstance(book["book_title"], str) for book in retrieved_user["loaned_books"])
    assert all(isinstance(book["description"], str) for book in retrieved_user["loaned_books"])
    assert all(isinstance(book["authors"], list) for book in retrieved_user["loaned_books"])
    assert all(isinstance(book["loan_date"], str) for book in retrieved_user["loaned_books"])
    assert all(isinstance(book["due_date"], str) for book in retrieved_user["loaned_books"])
    

def test_update_user_me(client, clean_db):
    """Prueba actualizar el usuario actual."""
    
    test_data = email_and_password_from_user_response()
    
    create_user(
        client,
        name="Update Me User",
        email=test_data["email"],
        password=test_data["password"],
        user_type="general",
        roles=["student"]
    )
    
    token = login_user(client, test_data["email"], test_data["password"])
    
    updated_info = {
        "name": "Updated Name",
        "email": f"updated_{test_data['email']}",
        "password": "NewPassword1234",
        "current_password": test_data["password"]
    }
    
    response = client.put(
        f"{BASE_URL}me",
        json=updated_info,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"Fallo al actualizar usuario: {response.status_code} - {response.text}"
    
    updated_user = response.json()
    
    assert updated_user["name"] == "Update Me User"
    assert updated_user["email"] == f"updated_{test_data['email']}"
    assert updated_user["user_type"] == "general"
    assert updated_user["roles"] == ["student"]
    
    assert "user_id" in updated_user
    assert "name" in updated_user
    assert "email" in updated_user
    assert "user_type" in updated_user
    assert "roles" in updated_user
    
    assert isinstance(updated_user["user_id"], str)
    assert isinstance(updated_user["name"], str)
    assert isinstance(updated_user["email"], str)
    assert isinstance(updated_user["user_type"], str)
    assert isinstance(updated_user["roles"], list)
   

def test_get_my_loan_history(client, clean_db):
    """Prueba obtener el historial de préstamos del usuario actual."""
    
    token = setup_login_successful(client, clean_db)
    
    response = client.get(
        f"{BASE_URL}me/loans",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200, f"Fallo al obtener historial de préstamos: {response.status_code} - {response.text}"
    
    loan_history = response.json()
    
    assert "user_id" in loan_history
    assert "user_name" in loan_history
    assert "loans" in loan_history
    
    assert isinstance(loan_history["user_id"], str)
    assert isinstance(loan_history["user_name"], str)
    assert isinstance(loan_history["loans"], list)
    
    assert all("loan_id" in loan for loan in loan_history["loans"])
    assert all("book_title" in loan for loan in loan_history["loans"])
    assert all("authors" in loan for loan in loan_history["loans"])
    assert all("loan_date" in loan for loan in loan_history["loans"])
    assert all("due_date" in loan for loan in loan_history["loans"])
    assert all("is_active" in loan for loan in loan_history["loans"])
    
    assert all(isinstance(loan["loan_id"], str) for loan in loan_history["loans"])
    assert all(isinstance(loan["book_title"], str) for loan in loan_history["loans"])
    assert all(isinstance(loan["authors"], list) for loan in loan_history["loans"])
    assert all(isinstance(loan["loan_date"], str) for loan in loan_history["loans"])
    assert all(isinstance(loan["due_date"], str) for loan in loan_history["loans"])
    assert all(isinstance(loan["is_active"], bool) for loan in loan_history["loans"])   



def test_delete_user_not_allowed(client, clean_db):
    """Prueba que la eliminación de un usuario no esté permitida."""
    
    test_data = email_and_password_from_user_response()
    
    user_data = create_user(
        client,
        name="Delete User",
        email=test_data["email"],
        password=test_data["password"],
        user_type="general",
        roles=["student"]
    )
    
    user_id = user_data["user_id"]
    token = login_user(client, test_data["email"], test_data["password"])
    
    response = client.delete(
        f"{BASE_URL}{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403, f"La eliminación de usuario debería no estar permitida: {response.status_code} - {response.text}"
    assert "Acceso denegado. Se requiere rol de administrador para eliminar usuarios." in response.text
    
    
def test_delete_user_successful(client, clean_db):
    """Prueba que la eliminación de un usuario SÍ esté permitida para un usuario administrador."""
    
    admin_data = email_and_password_from_user_response()
    target_data = email_and_password_from_user_response()
    
    create_user(
        client,
        name="Admin User",
        email=admin_data["email"],
        password=admin_data["password"],
        user_type="general",
        roles=["ADMIN"]
    )
    
    target_user_data = create_user(
        client, 
        name="Target User",
        email=target_data["email"],
        password=target_data["password"],
        user_type="general",
        roles=["student"]
    )
    
    target_user_id = target_user_data["user_id"]
    admin_token = login_user(client, admin_data["email"], admin_data["password"])
    
    response = client.delete(
        f"{BASE_URL}{target_user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204, f"Fallo al eliminar usuario: {response.status_code} - {response.text}"
    
    check_response = client.get(
        f"{BASE_URL}{target_user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert check_response.status_code == 404, "El usuario debería haber sido eliminado pero aún existe."
    