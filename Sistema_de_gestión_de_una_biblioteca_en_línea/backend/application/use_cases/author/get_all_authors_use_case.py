from typing import List
from domain.models.author import Author
from application.ports.author_repository import AuthorRepository

class GetAllAuthorsUseCase:
    
    def __init__(self, author_repository: AuthorRepository):
        self.author_repo = author_repository

    async def execute(self) -> List[Author]:
        
        return await self.author_repo.get_all()