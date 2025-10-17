from typing import List, Dict
from application.ports.book_repository import BookRepository
from domain.models.book import Book
from domain.models.author import Author
from application.ports.author_repository import AuthorRepository

class GetAllBooksUseCase:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.author_repository = author_repository
        self.book_repository = book_repository

    async def execute(self) -> List[Dict]:
        books: List[Book] = await self.book_repository.get_all()
        
        if not books:
            return []
        
        # 1. Recolectar todos los IDs de autores únicos de todos los libros
        all_author_ids = set()
        for book in books:
            all_author_ids.update(book.author)
            
        # 2. Consultar todos los autores únicos en una sola llamada eficiente
        all_authors: List[Author] = await self.author_repository.find_by_ids(list(all_author_ids))
        
        # 3. Mapear los autores a un diccionario para una búsqueda rápida O(1)
        author_map: Dict[str, Author] = {author.author_id: author for author in all_authors}
        
        # 4. Enriquecer la respuesta (List Comprehension para la transformación)
        enriched_books = []
        for book in books:
            # Enriquecer la lista de IDs con los nombres
            author_names = [
                author_map[author_id].name # <-- Aquí obtenemos el nombre
                for author_id in book.author
                if author_id in author_map # Solo si el autor fue encontrado
            ]
            
            # Devolver un diccionario simple para facilitar el mapeo en el controlador
            enriched_books.append({
                "isbn": book.isbn.value,
                "title": book.title.value,
                "author_names": author_names, # <-- Campo enriquecido (nombres)
                "description": book.description,
                "available_copies": book.available_copies
            })

        return enriched_books
        
        
        
