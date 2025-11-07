from typing import List
from domain.models.author import Author
from domain.ports.author_repository import AuthorRepository
from application.ports.author.get_all_author import GetAllAuthors

class GetAllAuthorsUseCase(GetAllAuthors):
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repo = author_repository

    async def get_all_authors(self) -> List[Author]:
        
        return await self.author_repo.get_all()
    
    