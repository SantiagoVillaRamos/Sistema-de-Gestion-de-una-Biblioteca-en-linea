import uuid
from domain.models.author import Author

class AuthorFactory:

    async def create(self, name: str, description: str) -> Author:
        
        author_id = str(uuid.uuid4())

        return Author(
            author_id=author_id,
            name=name,
            description=description
        )
