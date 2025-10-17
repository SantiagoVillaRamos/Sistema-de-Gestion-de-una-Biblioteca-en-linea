from domain.models.book import Book
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.author import Author

class BookMapper:
    
    @staticmethod
    def to_persistence(book: Book) -> dict:
        """
        Convierte un objeto de dominio Book a un diccionario para persistencia.
        """
        return {
            "book_id": book.book_id,
            "isbn": book.isbn.value,
            "title": book.title.value,
            "author": book.author,
            "description": book.description,
            "available_copies": book.available_copies
        }

    @staticmethod
    def to_domain(book_data: dict) -> Book:
        """
        Convierte un diccionario de persistencia a un objeto de dominio Book.
        """
        return Book(
            book_id=book_data['book_id'],
            isbn=ISBN(book_data['isbn']),
            title=Title(book_data['title']),
            author=book_data['author'],
            description=book_data['description'],
            available_copies=book_data['available_copies']
        )