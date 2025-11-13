from domain.models.user import User
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from typing import Optional
from infrastructure.persistence.models import UserModel

class UserMapper:
    """
    Clase responsable de mapear entre el objeto de dominio User
    y una representación para la persistencia (ej. un diccionario para una DB NoSQL o una fila de DB relacional).
    """

    @staticmethod
    def to_domain(persistence_data: dict) -> User:
        """Convierte un diccionario de datos de persistencia a un objeto de dominio User."""
        
        if persistence_data is None:
            return None
        
        if isinstance(persistence_data, dict):
            
            return User(
                user_id=persistence_data['user_id'],
                name=persistence_data['name'],
                email=Email(persistence_data['email']),
                password=Password(persistence_data['password']),
                user_type=persistence_data.get('user_type', 'general'),
                roles=persistence_data.get('roles', ['MEMBER']),
                is_active=persistence_data.get('is_active', True)
            )
            
        else:
            db_user = persistence_data
            return User(
                user_id=db_user.id,
                name=db_user.name,
                email=Email(db_user.email),
                password=Password(db_user.password_hash),
                user_type=db_user.user_type,
                roles=db_user.roles.split(",") if db_user.roles else [],
                is_active=db_user.is_active
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
        
    @staticmethod
    def to_db_model(domain_user: User, db_model: Optional[UserModel] = None) -> UserModel:
        """
        Convierte una Entidad de Dominio a un Modelo de DB de SQLAlchemy.
        Si se pasa un modelo existente (db_model), lo actualiza; si no, crea uno nuevo.
        """
        if db_model is None:
            db_model = UserModel(id=domain_user.user_id)
            
        db_model.name = domain_user.name
        db_model.email = str(domain_user.email.address) 
        db_model.password_hash = str(domain_user.password.hashed)
        db_model.user_type = domain_user.user_type
        db_model.roles = ",".join(domain_user.roles) 
        db_model.is_active = domain_user.is_active
        
        return db_model
        