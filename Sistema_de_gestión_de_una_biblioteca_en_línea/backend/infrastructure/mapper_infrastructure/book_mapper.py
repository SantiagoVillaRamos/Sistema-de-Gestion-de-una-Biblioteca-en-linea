from domain.models.book import Book
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.author import Author
from infrastructure.persistence.models import BookModel
from typing import Optional

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
    def to_domain(book_data: dict | BookModel) -> Book:
        """
        Convierte un diccionario de persistencia o Modelo DB a un objeto de dominio Book.
        """
        
        if book_data is None:
            return None
        
        if isinstance(book_data, dict):
            return Book(
                book_id=book_data['book_id'],
                isbn=ISBN(book_data['isbn']),
                title=Title(book_data['title']),
                author=book_data['author'],
                description=book_data['description'],
                available_copies=book_data['available_copies']
            )
        else:
            # Asumimos que es un objeto SQLAlchemy (BookModel)
            # Nota: book_data.author_id es un string, pero Book espera una lista.
            # Convertimos el ID único a una lista de un solo elemento.
            return Book(
                book_id=book_data.id,
                isbn=ISBN(book_data.isbn),
                title=Title(book_data.title),
                author=[book_data.author_id] if book_data.author_id else [],
                description=book_data.description,
                available_copies=book_data.available_copies
            )

    @staticmethod
    def to_db_model(domain_book: Book, db_model: Optional[BookModel] = None) -> BookModel:
        """
        Convierte una Entidad de Dominio a un Modelo de DB de SQLAlchemy.
        """
        if db_model is None:
            db_model = BookModel(id=domain_book.book_id)
            
        db_model.isbn = str(domain_book.isbn.value)
        db_model.title = str(domain_book.title.value)
        # Asumimos que el primer autor es el principal para el modelo de DB simple
        db_model.author_id = domain_book.author[0] if domain_book.author else None
        db_model.description = domain_book.description
        db_model.available_copies = domain_book.available_copies
        
        return db_model