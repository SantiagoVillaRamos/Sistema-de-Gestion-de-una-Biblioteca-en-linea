
from application.use_cases.author.create_author_use_case import CreateAuthorUseCase
from application.use_cases.author.get_all_authors_use_case import GetAllAuthorsUseCase
from application.use_cases.author.get_author_by_id_use_case import GetAuthorByIdUseCase
from application.use_cases.author.update_author_use_case import UpdateAuthorUseCase
from application.use_cases.author.delete_author_use_case import DeleteAuthorUseCase
from application.dto.author_command_dto import CreateAuthorCommand, UpdateAuthorCommand
from domain.models.author import Author
from domain.models.book import Book
from typing import List, Tuple

class AuthorFacade:
    
    def __init__(
        self, 
        create_use_case: CreateAuthorUseCase,
        get_all_use_case: GetAllAuthorsUseCase,
        get_by_id_use_case: GetAuthorByIdUseCase,
        update_use_case: UpdateAuthorUseCase,
        delete_author_data: DeleteAuthorUseCase
        
    ):
        self._create_author_use_case = create_use_case
        self._get_all_authors_use_case = get_all_use_case
        self._get_author_by_id_use_case = get_by_id_use_case
        self._update_use_case = update_use_case
        self._delete_author_data = delete_author_data

    async def create_author_facade(self, command: CreateAuthorCommand) -> Author:
        return await self._create_author_use_case.execute(command)


    async def get_all_authors(self) -> List[Author]:
        return await self._get_all_authors_use_case.execute()
    
    async def get_author_by_id(self, author_id: str) -> Tuple[Author, List[Book]]:
        return await self. _get_author_by_id_use_case.execute(author_id)
    
    async def update_author_data(self, author_id: str, command: UpdateAuthorCommand):
        return await self._update_use_case.execute(author_id, command)

    async def delete_author_data(self, author_id: str) -> None:
        return await self._delete_author_data.execute(author_id)
