from domain.models.author import Author
from domain.models.book import Book 
from typing import Tuple, List
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository

class GetAuthorByIdUseCase:
    
    def __init__(self, author_repository: AuthorRepository, book_repository: BookRepository):
        self.author_repo = author_repository
        self.book_repo = book_repository


    async def execute(self, author_id: str) -> Tuple[Author, List[Book]]: 
        
        author = await self.author_repo.find_by_id(author_id)
        
        books = await self.book_repo.find_by_author_id(author_id)
        
        return (author, books)