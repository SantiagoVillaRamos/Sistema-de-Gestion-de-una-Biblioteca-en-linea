from domain.models.author import Author
from domain.models.value_objects.author.author_name import AuthorName  
from domain.models.value_objects.author.author_description import AuthorDescription

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
    def to_domain(author_data: dict) -> Author:
        """
        Convierte un diccionario de persistencia a un objeto de dominio Author.
        """
        if author_data is None:
            return None
        
        return Author(
            author_id=author_data['author_id'],
            name=AuthorName(author_data['name']),
            description=AuthorDescription(author_data['description'])
        )
