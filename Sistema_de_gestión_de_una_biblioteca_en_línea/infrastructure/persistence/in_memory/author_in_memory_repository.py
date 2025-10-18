from typing import Dict, Optional, List
from application.ports.author_repository import AuthorRepository
from domain.models.author import Author
from infrastructure.mapper_infrastructure.author_mapper import AuthorMapper
from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError


class AuthorInMemoryRepository(AuthorRepository):
    
    def __init__(self):
        self._authors: Dict[str, dict] = {}

    async def save(self, author: Author) -> None:
        author_exists = any(a['name'] == author.name for a in self._authors.values())
        if author_exists:
            raise BusinessConflictError(author.name, "El autor con este nombre ya existe")
        persistence_data = AuthorMapper.to_persistence(author)
        self._authors[author.author_id] = persistence_data

    async def find_by_id(self, author_id: str) -> Optional[Author]:
        persistence_data = self._authors.get(author_id)
        if not persistence_data:
            raise BusinessNotFoundError(author_id, "El ID no existe")
        return AuthorMapper.to_domain(persistence_data)
    

    async def get_all(self) -> List[Author]:
        if not self._authors:
            return []
        return [AuthorMapper.to_domain(data) for data in self._authors.values()]

    async def find_by_name(self, name: str) -> Optional[Author]:
        for data in self._authors.values():
            if data['name'] == name:
                return AuthorMapper.to_domain(data)
        return BusinessNotFoundError(name, f"El nombre no existe")
    
    async def find_by_ids(self, author_ids: List[str]) -> List[Author]:
        
        # 1. Recuperar los datos de persistencia (diccionarios) para los IDs dados.
        #    Solo incluimos datos si el ID existe en el diccionario _authors.
        authors_data = [
            self._authors[author_id] 
            for author_id in author_ids 
            if author_id in self._authors
        ]
        
        # 2. Mapear los datos de persistencia a las Entidades de Dominio (Author).
        #    Usamos AuthorMapper.to_domain para la conversión.
        domain_authors = [
            AuthorMapper.to_domain(data) 
            for data in authors_data
        ]
    
        return domain_authors
