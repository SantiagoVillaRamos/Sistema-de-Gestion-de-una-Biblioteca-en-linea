import uuid
from domain.models.author import Author
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription

class AuthorFactory:

    @staticmethod
    def create(name: str, description: str) -> Author:
        
        author_id = str(uuid.uuid4())
        name_vo = AuthorName(name)
        description_vo = AuthorDescription(description)

        return Author(
            author_id=author_id,
            name=name_vo,
            description=description_vo
        )
