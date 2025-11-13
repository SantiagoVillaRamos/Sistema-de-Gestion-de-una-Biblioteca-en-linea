from domain.models.author import Author
from domain.ports.author_repository import AuthorRepository
from application.dto.author_command_dto import CreateAuthorCommand
from domain.models.factory.authorFactory import AuthorFactory
from application.ports.author.create_author import CreateAuthor
from domain.models.exceptions.business_exception import BusinessConflictError

class CreateAuthorUseCase(CreateAuthor):
    
    def __init__(self, author_repository: AuthorRepository, author_factory:AuthorFactory):
        self.author_repo = author_repository
        self.author_factory = author_factory
        
    async def create_author(self, command: CreateAuthorCommand) -> Author:
        
        author_exists = await self.author_repo.find_by_name(command.name)
        if author_exists:
            raise BusinessConflictError(command.name, "El autor con este nombre ya existe")
        
        new_author: Author = self.author_factory.create(
            name=command.name,
            description=command.description
        )
        
        await self.author_repo.save(new_author)

        return new_author
