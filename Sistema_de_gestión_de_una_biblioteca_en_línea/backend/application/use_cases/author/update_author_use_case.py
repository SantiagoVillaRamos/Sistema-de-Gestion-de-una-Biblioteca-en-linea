
from domain.models.author import Author
from application.dto.author_command_dto import UpdateAuthorCommand
from domain.models.value_objects.author.author_name import AuthorName
from domain.models.value_objects.author.author_description import AuthorDescription
from application.ports.author_repository import AuthorRepository


class UpdateAuthorUseCase:
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repo = author_repository

    async def execute(self, author_id: str, command: UpdateAuthorCommand) -> Author:
        # 1. Cargar el Agregado Raíz
        author: Author = await self.author_repo.find_by_id(author_id)
        
        # 2. Preparar los nuevos VOs solo si los datos están presentes
        new_name_vo = author.name
        new_description_vo = author.description
        
        if command.name is not None:
            # La creación del VO lanza BusinessTypeError si es inválido (ej. string vacío)
            new_name_vo = AuthorName(value=command.name)
            
        if command.description is not None:
            new_description_vo = AuthorDescription(value=command.description)

        # 3. Llamar al método de Dominio (update_profile)
        author.update_profile(new_name=new_name_vo, new_description=new_description_vo)
        
        # 4. Persistir los cambios
        await self.author_repo.update(author) 
        
        return author
    
