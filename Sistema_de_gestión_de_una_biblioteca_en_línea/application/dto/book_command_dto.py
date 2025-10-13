from dataclasses import dataclass

@dataclass(frozen=True)
class CreateBookCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un libro.
    """
    isbn: str
    title: str
    author_id: str
    description: str
    available_copies: int

@dataclass(frozen=True)
class CreateBookResponse:
    """
    DTO para los datos de salida del caso de uso de crear un libro.
    """
    book_id: str
    isbn: str
    title: str
    author_id: str
    description: str