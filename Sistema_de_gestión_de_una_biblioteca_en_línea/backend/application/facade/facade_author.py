
from application.ports.author.create_author import CreateAuthor
from application.ports.author.delete_author import DeleteAuthor
from application.ports.author.get_all_author import GetAllAuthors
from application.ports.author.get_author_by_id import GetAuthorByID
from application.ports.author.update_author import UpdateAuthor

from application.dto.author_command_dto import CreateAuthorCommand, UpdateAuthorCommand, GetAuthorDetailsResult
from domain.models.author import Author
from typing import List

class AuthorFacade:
    
    def __init__(
        self, 
        create_use_case: CreateAuthor,
        get_all_use_case: GetAllAuthors,
        get_by_id_use_case: GetAuthorByID,
        update_use_case: UpdateAuthor,
        delete_author_data: DeleteAuthor
        
    ):
        self._create_author_use_case = create_use_case
        self._get_all_authors_use_case = get_all_use_case
        self._get_author_by_id_use_case = get_by_id_use_case
        self._update_use_case = update_use_case
        self._delete_author_data = delete_author_data

    async def create_author_facade(self, command: CreateAuthorCommand) -> Author:
        return await self._create_author_use_case.create_author(command)


    async def get_all_authors(self) -> List[Author]:
        return await self._get_all_authors_use_case.get_all_authors()
    
    async def get_author_by_id(self, author_id: str) -> GetAuthorDetailsResult:
        return await self. _get_author_by_id_use_case.get_author_by_id(author_id)
    
    async def update_author_data(self, author_id: str, command: UpdateAuthorCommand):
        return await self._update_use_case.update_author(author_id, command)

    async def delete_author_data(self, author_id: str) -> None:
        return await self._delete_author_data.delete_author(author_id)
