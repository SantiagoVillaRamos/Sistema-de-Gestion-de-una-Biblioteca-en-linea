from __future__ import annotations
from dataclasses import dataclass, field
from domain.value_objects.isbn import ISBN
from domain.value_objects.title import Title
import uuid


from domain.exceptions.book import BookNotFoundError

@dataclass
class Book:
    
    book_id: str
    isbn: ISBN
    title: Title
    author: str
    available_copies: int

    def __post_init__(self):
        
        if self.available_copies < 0:
            raise BookNotFoundError(self.available_copies, "No hay copias disponibles")

    def lend(self) -> None:
        """
        Reduce el número de copias disponibles.
        """
        if self.available_copies <= 0:
            raise BookNotFoundError(self.available_copies, "No hay copias disponibles")
        self.available_copies -= 1

    def return_book(self) -> None:
        """
        Aumenta el número de copias disponibles.
        """
        self.available_copies += 1
        
    def is_available(self) -> bool:
        """
        Verifica si hay copias disponibles para prestar.
        """
        return self.available_copies > 0
        