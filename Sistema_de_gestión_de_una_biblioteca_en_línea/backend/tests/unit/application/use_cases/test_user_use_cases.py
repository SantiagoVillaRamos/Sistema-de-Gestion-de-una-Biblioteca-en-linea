import pytest
from domain.models.user import User
from application.use_cases.user.create_user_use_case import CreateUserUseCase
import uuid



@pytest.mark.asyncio
async def test_create_user_success(create_user_command, use_case_dependencies):
    """Prueba la ejecución exitosa del caso de uso CreateUserUseCase."""

    # 1. Setup: Desempaquetar dependencias
    mock_repo, mock_factory = use_case_dependencies
    
    # 2. Crear la entidad de usuario que esperamos que devuelva el Factory
    user_id = str(uuid.uuid4())
    expected_user = User(
        user_id=user_id,
        name=create_user_command.name,
        email=create_user_command.email,
        password=create_user_command.password,
        user_type=create_user_command.user_type,
        roles=create_user_command.roles
    )

    # 3. Configurar el Mock del Factory para que devuelva la entidad esperada
    mock_factory.create.return_value = expected_user
    
    # 4. Instanciar el Caso de Uso
    use_case = CreateUserUseCase(
        user_repository=mock_repo,
        user_factory=mock_factory
    )
    
    # 5. Ejecutar (Act)
    result_user = await use_case.execute(create_user_command)
    
    # 6. Aserciones (Assert)

    # A1. Verificar que el Factory fue llamado correctamente (Lógica de creación)
    mock_factory.create.assert_called_once_with(
        name=create_user_command.name,
        email=create_user_command.email,
        password=create_user_command.password,
        user_type=create_user_command.user_type,
        roles=create_user_command.roles
    )
    
    # A2. Verificar que el Repositorio fue llamado para guardar el objeto correcto
    mock_repo.save.assert_called_once_with(expected_user)
    
    # A3. Verificar que el resultado de la ejecución sea el objeto User esperado
    assert result_user == expected_user
    assert result_user.email == create_user_command.email
    assert result_user.name == create_user_command.name
    assert result_user.password == create_user_command.password
    assert result_user.user_type == create_user_command.user_type
    assert result_user.roles == create_user_command.roles
    
    assert isinstance(result_user.name, str)
    assert isinstance(result_user.email, str)
    assert isinstance(result_user.password, str)
    assert isinstance(result_user.user_type, str)
    assert isinstance(result_user.roles, list)