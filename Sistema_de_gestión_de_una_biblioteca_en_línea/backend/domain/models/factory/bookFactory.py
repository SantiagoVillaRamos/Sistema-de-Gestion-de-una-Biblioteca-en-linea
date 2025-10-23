import uuid
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.book import Book
from typing import List


class BookFactory:
   
    @staticmethod
    def create(isbn: str, title: str, author: List[str], description: str, available_copies: int) -> Book:
        
        book_id = str(uuid.uuid4())
        
        return Book(
            book_id=book_id,
            isbn=ISBN(isbn),
            title=Title(title),
            author=author,
            description=description,
            available_copies=available_copies
        )
        
        