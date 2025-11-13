from domain.models.author import Author
from domain.models.value_objects.author.author_name import AuthorName  
from domain.models.value_objects.author.author_description import AuthorDescription
from typing import Optional
from infrastructure.persistence.models import AuthorModel

class AuthorMapper:
    
    @staticmethod
    def to_persistence(author: Author) -> dict:
        """
        Convierte un objeto de dominio Author a un diccionario para persistencia.
        """
        return {
            "author_id": author.author_id,
            "name": author.name.value,
            "description": author.description.value
        }


    @staticmethod
    def to_domain(persistence_data: dict) -> Author:
        """
        Convierte un diccionario de persistencia a un objeto de dominio Author.
        """
        if persistence_data is None:
            return None
        
        if isinstance(persistence_data, dict):
            return Author(
                author_id=persistence_data['author_id'],
                name=AuthorName(persistence_data['name']),
                description=AuthorDescription(persistence_data['description'])
            )
        else:
            db_author = persistence_data
            return Author(
                author_id=db_author.id,
                name=AuthorName(db_author.name),
                description=AuthorDescription(db_author.description if hasattr(db_author, 'description') else None) 
            )    
        
    @staticmethod
    def to_db_model(domain_author: Author, db_model: Optional[AuthorModel] = None) -> AuthorModel:
        """
        Convierte una Entidad de Dominio a un Modelo de DB de SQLAlchemy.
        Si se pasa un modelo existente (db_model), lo actualiza; si no, crea uno nuevo.
        """
        if db_model is None:
            db_model = AuthorModel(id=domain_author.author_id)
            
        db_model.name = str(domain_author.name.value)
        db_model.description = str(domain_author.description.value)
        
        return db_model
    
    