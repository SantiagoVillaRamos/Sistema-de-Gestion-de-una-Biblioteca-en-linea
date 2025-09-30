import uuid
from domain.value_objects.isbn import ISBN
from domain.value_objects.title import Title
from domain.entities.book import Book


class BookFactory:
    @staticmethod
    def create(isbn: str, title: str, author: str, available_copies: int) -> Book:
        
        book_id = str(uuid.uuid4())
        
        return Book(
            book_id=book_id,
            isbn=ISBN(isbn),
            title=Title(title),
            author=author,
            available_copies=available_copies
        )