from typing import List, Dict, Set, Any
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
        
        # Obtener el mapa de IDs de autor a Entidades Author ({id: Author_Entity})
        author_map: Dict[str, Author] = await self._collect_all_author_data(books)
        
        enriched_books = self._enrich_the_answer(books, author_map)
        
        return enriched_books
    
        
    async def _collect_all_author_data(self, books: List[Book]) -> Dict[str, Author]:
        """Recolectar todos los IDs de autores únicos de todos los libros"""
        
        # 1. Recolectar todos los IDs de autores únicos de todos los libros
        all_author_ids: Set[str] = set()
        for book in books:
            all_author_ids.update(book.author)
        
        # Si no hay IDs de autores, devolver un mapa vacío.
        if not all_author_ids:
            return {}    
        
        # 2. Consultar todos los autores únicos en una sola llamada eficiente
        all_authors: List[Author] = await self.author_repository.find_by_ids(list(all_author_ids))
        
        # 3. Mapear los autores a un diccionario para una búsqueda rápida O(1)
        author_map: Dict[str, Author] = {author.author_id: author for author in all_authors}
        return author_map
        
    
    def _enrich_the_answer(self, books: List[Book], author_map: Dict[str, Author]) -> List[Dict[str, Any]]:
        """Enriquecer la respuesta (List Comprehension para la transformación)"""
        
        # 4. Enriquecer la respuesta
        enriched_books: List[Dict[str, Any]] = []
        for book in books:
            # Enriquecer la lista de IDs con los nombres
            author_names = [
                author_map[author_id].name 
                for author_id in book.author
                if author_id in author_map 
            ]
            
            # Devolver un diccionario simple para facilitar el mapeo en el controlador
            enriched_books.append({
                "isbn": book.isbn.value,
                "title": book.title.value,
                "author_names": author_names,
                "description": book.description,
                "available_copies": book.available_copies
            })

        return enriched_books