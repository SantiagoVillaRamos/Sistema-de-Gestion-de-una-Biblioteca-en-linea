from typing import Dict, Optional, List
from domain.ports.author_repository import AuthorRepository
from domain.models.author import Author
from infrastructure.mapper_infrastructure.author_mapper import AuthorMapper


class AuthorInMemoryRepository(AuthorRepository):
    
    def __init__(self):
        self._authors: Dict[str, dict] = {}

    async def save(self, author: Author) -> None:
        persistence_data = AuthorMapper.to_persistence(author)
        self._authors[author.author_id] = persistence_data
        

    async def find_by_id(self, author_id: str) -> Optional[Author]:
        persistence_data = self._authors.get(author_id)
        return AuthorMapper.to_domain(persistence_data)
    

    async def get_all(self) -> List[Author]:
        if not self._authors:
            return []
        return [AuthorMapper.to_domain(data) for data in self._authors.values()]

    async def find_by_name(self, name: str) -> Optional[Author]:
        for data in self._authors.values():
            if data['name'] == name:
                return AuthorMapper.to_domain(data)
        return None
    
    
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

    async def update(self, author: Author) -> None:

        updated_data = AuthorMapper.to_persistence(author)
        self._authors[author.author_id] = updated_data


    async def delete(self, author_id: str) -> None:
        del self._authors[author_id]
