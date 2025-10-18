
from application.use_cases.author.create_author_use_case import CreateAuthorUseCase
from application.use_cases.author.get_all_authors_use_case import GetAllAuthorsUseCase
from application.use_cases.author.get_author_by_id_use_case import GetAuthorByIdUseCase
from application.dto.author_command_dto import CreateAuthorCommand
from domain.models.author import Author
from domain.models.book import Book
from typing import List, Tuple

class AuthorFacade:
    
    def __init__(
        self, 
        create_use_case: CreateAuthorUseCase,
        get_all_use_case: GetAllAuthorsUseCase,
        get_by_id_use_case: GetAuthorByIdUseCase
        
    ):
        self._create_author_use_case = create_use_case
        self._get_all_authors_use_case = get_all_use_case
        self._get_author_by_id_use_case = get_by_id_use_case

    async def create_author_facade(self, command: CreateAuthorCommand) -> Author:
        return await self._create_author_use_case.execute(command)


    async def get_all_authors(self) -> List[Author]:
        return await self._get_all_authors_use_case.execute()
    
    async def get_author_by_id(self, author_id: str) -> Tuple[Author, List[Book]]:
        return await self. _get_author_by_id_use_case.execute(author_id)
    
