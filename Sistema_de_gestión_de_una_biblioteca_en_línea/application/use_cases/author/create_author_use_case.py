from domain.models.author import Author
from application.ports.author_repository import AuthorRepository
from application.dto.author_command_dto import CreateAuthorCommand, CreateAuthorResponse
from domain.models.factory.authorFactory import AuthorFactory

class CreateAuthorUseCase:
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repo = author_repository
        self.author_factory = AuthorFactory()

    async def execute(self, command: CreateAuthorCommand) -> CreateAuthorResponse:
        
        new_author = await self.author_factory.create(
            name=command.name,
            description=command.description
        )
        
        await self.author_repo.save(new_author)

        return self._build_author_response(new_author)
    
    def _build_author_response(self, new_author: Author) -> CreateAuthorResponse:   
        
        return CreateAuthorResponse(
            author_id=new_author.author_id,
            name=new_author.name,
            description=new_author.description
        )
