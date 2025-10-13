from domain.models.author import Author

class AuthorMapper:
    
    @staticmethod
    def to_persistence(author: Author) -> dict:
        """
        Convierte un objeto de dominio Author a un diccionario para persistencia.
        """
        return {
            "author_id": author.author_id,
            "name": author.name,
            "description": author.description
        }

    @staticmethod
    def to_domain(author_data: dict) -> Author:
        """
        Convierte un diccionario de persistencia a un objeto de dominio Author.
        """
        return Author(
            author_id=author_data['author_id'],
            name=author_data['name'],
            description=author_data['description']
        )
