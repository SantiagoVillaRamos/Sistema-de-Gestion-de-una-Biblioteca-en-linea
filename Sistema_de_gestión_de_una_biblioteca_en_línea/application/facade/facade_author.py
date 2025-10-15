from application.ports.author_repository import AuthorRepository
from application.use_cases.author.create_author_use_case import CreateAuthorUseCase
from application.dto.author_command_dto import CreateAuthorCommand, CreateAuthorResponse

class AuthorFacade:
    
    def __init__(self, author_repo: CreateAuthorUseCase):
        self._create_author_use_case = author_repo

    async def create_author_facade(self, command: CreateAuthorCommand) -> CreateAuthorResponse:
        return await self._create_author_use_case.execute(command)
