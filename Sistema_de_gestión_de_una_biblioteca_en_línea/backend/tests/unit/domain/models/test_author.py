import pytest
from domain.models.value_objects.author.author_name import AuthorName  
from domain.models.value_objects.author.author_description import AuthorDescription
from domain.models.exceptions.business_exception import BusinessTypeError 
from domain.models.author import Author


def test_author_name_creation_success():
    """Prueba que AuthorName se crea correctamente y estandariza el valor."""
    # Arrange & Act
    name = AuthorName(value=" robert c. martin ")
    
    # Assert
    assert name.value == "Robert C. Martin"
    assert isinstance(name, AuthorName)

def test_author_name_creation_failure_empty():
    """Prueba que AuthorName falla si el valor es None o vacío."""
    # Arrange & Act & Assert: Debe levantar una excepción por nombre vacío
    with pytest.raises(BusinessTypeError, match="El nombre del autor no puede estar vacío."):
        AuthorName(value="")

def test_author_name_creation_failure_spaces():
    """Prueba que AuthorName falla si el valor es solo espacios."""
    # Arrange & Act & Assert: Debe levantar una excepción por nombre vacío
    with pytest.raises(BusinessTypeError, match="El nombre del autor no puede estar vacío."):
        AuthorName(value="   ")

def test_author_name_creation_failure_too_long():
    """Prueba que AuthorName falla si excede los 100 caracteres."""
    long_name = "A" * 101 # 101 caracteres
    
    # Arrange & Act & Assert: Debe levantar una excepción por exceso de longitud
    with pytest.raises(BusinessTypeError, match="El nombre del autor no puede exceder los 100 caracteres."):
        AuthorName(value=long_name)

# --- 2. Pruebas para AuthorDescription ---

def test_author_description_creation_success():
    """Prueba que AuthorDescription se crea correctamente y maneja espacios."""
    # Arrange & Act
    description = AuthorDescription(value="  Descripción breve del autor. ")
    
    # Assert
    assert description.value == "Descripción breve del autor."
    assert isinstance(description, AuthorDescription)

def test_author_description_handles_none_value():
    """Prueba que AuthorDescription convierte None en cadena vacía."""
    # Arrange & Act
    description = AuthorDescription(value=None)
    
    # Assert
    assert description.value == ''

def test_author_description_handles_empty_value():
    """Prueba que AuthorDescription maneja cadenas vacías o solo espacios."""
    # Arrange & Act
    description_empty = AuthorDescription(value="")
    description_spaces = AuthorDescription(value="   ")
    
    # Assert
    assert description_empty.value == ""
    assert description_spaces.value == ""

def test_author_description_creation_failure_too_long():
    """Prueba que AuthorDescription falla si excede los 500 caracteres."""
    long_description = "B" * 501 # 501 caracteres
    
    # Arrange & Act & Assert: Debe levantar una excepción por exceso de longitud
    with pytest.raises(BusinessTypeError, match="La descripción del autor no puede exceder los 500 caracteres."):
        AuthorDescription(value=long_description)



def test_author_update_profile_success(existing_author: Author):
    """Prueba que el perfil del autor se actualiza correctamente."""
    # Arrange
    old_name_value = existing_author.get_name_value()
    new_name = AuthorName(value="Maria Antonieta")
    new_description = AuthorDescription(value="Poeta del siglo XX.")
    
    # Act
    existing_author.update_profile(new_name, new_description)
    
    # Assert
    # Se actualizan los VOs
    assert existing_author.name == new_name
    assert existing_author.description == new_description
    # El valor primitivo es el esperado (y estandarizado por el VO)
    assert existing_author.get_name_value() == "Maria Antonieta"
    # El ID debe permanecer inalterado
    assert isinstance(existing_author.author_id, str)

def test_author_update_profile_fails_on_invalid_input(existing_author: Author):
    """
    Prueba que el método de actualización falla si los nuevos VOs son inválidos,
    ya que la creación de VOs debe levantar la excepción antes de la asignación.
    """
    # Arrange
    invalid_name_str = " " # Un nombre que el VO Name rechazará
    
    # Act & Assert
    with pytest.raises(BusinessTypeError, match="El nombre del autor no puede estar vacío."):
        # Intentamos crear el nuevo VO inválido
        invalid_name = AuthorName(value=invalid_name_str)
        # La asignación (update_profile) ni siquiera debería ser alcanzada
        existing_author.update_profile(invalid_name, existing_author.description)
        
    # Assert 2 (Verificar que el estado original no fue modificado)
    # Si la excepción se levantó en la creación del VO, el estado original debe ser el mismo.
    assert existing_author.name.value == "Robert C. Martin"
    
def test_author_get_name_value_helper(existing_author: Author):
    """Prueba el helper get_name_value."""
    assert existing_author.get_name_value() == "Robert C. Martin"

