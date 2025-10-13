import uuid
from domain.models.author import Author

class AuthorFactory:
   
    @staticmethod
    def create(name: str, description: str) -> Author:
        
        author_id = str(uuid.uuid4())
        
        return Author(
            author_id=author_id,
            name=name,
            description=description
        )
