from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.exceptions.business_exception import BusinessNotFoundError, BusinessConflictError
from domain.models.user import User

import pytest
import uuid


# --- 1. Pruebas para Email (Value Object) ---

def test_email_creation_success(valid_email: Email):
    """Prueba la creación exitosa de un Email y su normalización."""
    # Arrange & Act
    email = valid_email
    
    # Assert
    assert email.address == "usuario.prueba@gmail.com"
    assert isinstance(email, Email)


@pytest.mark.parametrize("invalid_address", [
    "",
    "   ",
    "user@domain.net", # Dominio no permitido
    "invalid-format.com", # Sin @
    "user@gmail", # Dominio incompleto
    None # Aunque Python permite None, la validación interna debería atraparlo como vacío
])
def test_email_creation_failure_invalid_format_or_domain(invalid_address):
    """Prueba que Email falla con formatos inválidos o dominios no permitidos."""
    with pytest.raises(BusinessConflictError, match="Dirección de correo electrónico inválida."):
        # Act
        Email(address=invalid_address)

# --- 2. Pruebas para Password (Value Object) ---

def test_password_creation_success(valid_password: Password):
    """Prueba que Password se crea correctamente (asumiendo que el hash ya fue generado)."""
    # Assert solo comprueba la existencia del objeto
    assert isinstance(valid_password, Password)
    assert valid_password.hashed == "random-hash-string-1234"


# --- 3. Pruebas para la Entidad User (Lógica de Negocio) ---

def test_user_creation_success(existing_user: User):
    """Prueba la creación exitosa de un usuario y la normalización del nombre."""
    # Assert
    assert existing_user.user_type == "general"
    assert existing_user.is_active is True
    # Verifica la normalización del nombre
    assert existing_user.name == "Elena García"
    assert isinstance(existing_user.email, Email)

@pytest.mark.parametrize("invalid_name", [
    "",
    "  ",
    None 
])
def test_user_creation_failure_empty_name(invalid_name, valid_email, valid_password):
    """Prueba que la creación falla si el nombre está vacío o solo contiene espacios."""
    # Arrange
    email = valid_email
    password = valid_password
    
    # Act & Assert
    with pytest.raises(BusinessNotFoundError, match="El nombre no puede estar vacío."):
        User(
            user_id=str(uuid.uuid4()),
            name=invalid_name, # Este valor causa el fallo en __post_init__
            email=email,
            password=password,
            user_type="general",
            roles=[]
        )

def test_user_deactivate_success(existing_user: User):
    """Prueba que el método deactivate cambia el estado a False."""
    # Arrange
    assert existing_user.is_active is True
    
    # Act
    existing_user.deactivate()
    
    # Assert
    assert existing_user.is_active is False

def test_user_activate_success(existing_user: User):
    """Prueba que el método activate cambia el estado a True."""
    # Arrange: Desactivamos primero para probar la activación
    existing_user.deactivate()
    assert existing_user.is_active is False

    # Act
    existing_user.activate()
    
    # Assert
    assert existing_user.is_active is True