
from domain.models.author import Author
from application.dto.author_command_dto import UpdateAuthorCommand
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription
from domain.ports.author_repository import AuthorRepository
from application.ports.author.update_author import UpdateAuthor
from domain.models.exceptions.business_exception import BusinessNotFoundError

class UpdateAuthorUseCase(UpdateAuthor):
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repo = author_repository

    async def update_author(self, author_id: str, command: UpdateAuthorCommand) -> Author:
        
        author: Author = await self.author_repo.find_by_id(author_id)
        if not author:
            raise BusinessNotFoundError(author_id, "No existe el ID.")
        
        # Preparar los nuevos VOs solo si los datos están presentes
        new_name_vo = author.name
        new_description_vo = author.description
        
        if command.name is not None:
            # La creación del VO lanza BusinessTypeError si es inválido (ej. string vacío)
            new_name_vo = AuthorName(value=command.name)
            
        if command.description is not None:
            new_description_vo = AuthorDescription(value=command.description)

        author.update_profile(new_name=new_name_vo, new_description=new_description_vo)
       
        await self.author_repo.update(author) 
        
        return author
    
