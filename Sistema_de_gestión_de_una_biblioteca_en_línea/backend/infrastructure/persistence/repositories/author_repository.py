from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime

# Importaciones de Infraestructura
from infrastructure.persistence.models import AuthorModel
# Importaciones de Dominio (Puertos y Entidades)
from domain.ports.author_repository import AuthorRepository

from domain.models.author import Author
# Asumo que estos están en domain.models...
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.value_objects.due_date import DueDate
from domain.models.exceptions.business_exception import BusinessNotFoundError 

# --- REPOSITORIO DE AUTOR ---
class SQLAlchemyAuthorRepository(AuthorRepository): # CORREGIDO: Hereda del Puerto
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _map_to_domain(self, db_author: AuthorModel) -> Optional[Author]:
        if not db_author:
            return None
        # Asumo que la Entidad Autor solo necesita id y nombre
        return Author(id=db_author.id, name=db_author.name)

    async def save(self, author: Author) -> None: # CORREGIDO: Async
        # La lógica de creación/actualización debe ser robusta para el ORM 
        db_author = await self.session.get(AuthorModel, author.id)
        
        if db_author:
            # Actualización
            db_author.name = author.name
        else:
            # Creación
            db_author = AuthorModel(id=author.id, name=author.name)
            self.session.add(db_author)
            
        try:
            await self.session.commit()
            await self.session.refresh(db_author)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def find_by_id(self, author_id: str) -> Optional[Author]: # CORREGIDO: Async
        db_author = await self.session.get(AuthorModel, author_id)
        return await self._map_to_domain(db_author)

    async def get_all(self) -> List[Author]: # CORREGIDO: Async
        stmt = select(AuthorModel)
        result = await self.session.execute(stmt)
        db_authors = result.scalars().all()
        return [await self._map_to_domain(a) for a in db_authors]

    async def find_by_name(self, name: str) -> Optional[Author]: # CORREGIDO: Async
        stmt = select(AuthorModel).where(AuthorModel.name == name)
        result = await self.session.execute(stmt)
        db_author = result.scalars().first()
        return await self._map_to_domain(db_author)

    async def find_by_ids(self, author_ids: List[str]) -> List[Author]: # CORREGIDO: Async
        stmt = select(AuthorModel).where(AuthorModel.id.in_(author_ids))
        result = await self.session.execute(stmt)
        db_authors = result.scalars().all()
        return [await self._map_to_domain(a) for a in db_authors]
    
    async def update(self, author: Author) -> None: # CORREGIDO: Async
        # Mismo código que save para persistencia del Agregado
        await self.save(author)

    async def delete(self, author_id: str) -> None: # CORREGIDO: Async
        stmt = delete(AuthorModel).where(AuthorModel.id == author_id)
        await self.session.execute(stmt)
        await self.session.commit()