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
        return User(
            user_id=persistence_data['user_id'],
            name=persistence_data['name'],
            email=Email(persistence_data['email']),
            password=Password(persistence_data['password']),
            is_active=persistence_data['is_active'],
            user_type=persistence_data['user_type']
        )

    @staticmethod
    def to_persistence(domain_user: User) -> dict:
        """Convierte un objeto de dominio User a un diccionario para persistencia."""
        return {
            "user_id": domain_user.user_id,
            "name": domain_user.name,
            "email": domain_user.email.address,
            "password": domain_user.password.hashed,
            "is_active": domain_user.is_active,
            "user_type": domain_user.user_type
        
        }