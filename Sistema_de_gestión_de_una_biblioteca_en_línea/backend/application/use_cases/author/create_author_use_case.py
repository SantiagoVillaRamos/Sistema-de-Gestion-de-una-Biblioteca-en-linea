from domain.models.author import Author
from domain.ports.author_repository import AuthorRepository
from application.dto.author_command_dto import CreateAuthorCommand
from domain.models.factory.authorFactory import AuthorFactory

class CreateAuthorUseCase:
    
    def __init__(self, author_repository: AuthorRepository, author_factory:AuthorFactory):
        self.author_repo = author_repository
        self.author_factory = author_factory
        
    async def execute(self, command: CreateAuthorCommand) -> Author:
        
        new_author: Author = self.author_factory.create(
            name=command.name,
            description=command.description
        )
        
        await self.author_repo.save(new_author)

        return new_author
