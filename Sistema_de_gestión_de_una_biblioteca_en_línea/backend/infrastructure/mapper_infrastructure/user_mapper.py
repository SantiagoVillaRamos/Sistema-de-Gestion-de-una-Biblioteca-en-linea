from domain.models.user import User
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password


class UserMapper:
    """
    Clase responsable de mapear entre el objeto de dominio User
    y una representación para la persistencia (ej. un diccionario para una DB NoSQL o una fila de DB relacional).
    """

    @staticmethod
    def to_domain(persistence_data: dict) -> User:
        """Convierte un diccionario de datos de persistencia a un objeto de dominio User."""
        # Al reconstruir, el password ya está hasheado. Lo pasamos directamente.
        # El Value Object Password se usa para hashear, no para almacenar un hash.
        return User(
            user_id=persistence_data['user_id'],
            name=persistence_data['name'],
            email=Email(persistence_data['email']),
            password=Password(persistence_data['password']),
            user_type=persistence_data.get('user_type', 'general'),
            roles=persistence_data.get('roles', ['MEMBER']),
            is_active=persistence_data.get('is_active', True)
        )


    @staticmethod
    def to_persistence(domain_user: User) -> dict:
        """Convierte un objeto de dominio User a un diccionario para persistencia."""
        return {
            "user_id": domain_user.user_id,
            "name": domain_user.name,
            "email": domain_user.email.address,
            "password": domain_user.password.hashed,
            "user_type": domain_user.user_type,
            "roles": domain_user.roles,
            "is_active": domain_user.is_active,
        }