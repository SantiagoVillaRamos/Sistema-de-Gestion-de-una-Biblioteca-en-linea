from __future__ import annotations
from dataclasses import dataclass
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title



from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass
class Book:
    
    book_id: str
    isbn: ISBN
    title: Title
    author: str
    available_copies: int

    def __post_init__(self):
        
        if self.available_copies <= 0:
            raise BusinessNotFoundError(self.available_copies, "No hay copias disponibles")


    def lend(self) -> None:
        
        if self.available_copies <= 0:
            raise BusinessNotFoundError(self.available_copies, "No hay copias disponibles")
        self.available_copies -= 1


    def return_book(self) -> None:
        self.available_copies += 1
        
        
    def is_available(self) -> bool:
        return self.available_copies > 0
        