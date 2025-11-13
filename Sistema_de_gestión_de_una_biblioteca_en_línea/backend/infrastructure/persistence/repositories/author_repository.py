from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from infrastructure.persistence.models import AuthorModel
from infrastructure.mapper_infrastructure.author_mapper import AuthorMapper
from domain.ports.author_repository import AuthorRepository
from domain.models.author import Author
from domain.models.exceptions.business_exception import BusinessError 

# --- REPOSITORIO DE AUTOR ---
class SQLAlchemyAuthorRepository(AuthorRepository):
    """
    Adaptador que implementa el Puerto AuthorRepository utilizando 
    SQLAlchemy con un driver PostgreSQL asíncrono.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, author: Author) -> None: 
        
        db_author = await self.session.get(AuthorModel, author.author_id)
        
        db_author_mapper = AuthorMapper.to_db_model(author, db_author)
        
        if not await self.session.get(AuthorModel, author.author_id):
            self.session.add(db_author_mapper)
            
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise BusinessError(f"Error: {e}")


    async def find_by_id(self, author_id: str) -> Optional[Author]: 
        db_author = await self.session.get(AuthorModel, author_id)
        return AuthorMapper.to_domain(db_author)

    async def get_all(self) -> List[Author]: 
        stmt = select(AuthorModel)
        result = await self.session.execute(stmt)
        db_authors = result.scalars().all()
        return [AuthorMapper.to_domain(a) for a in db_authors]

    async def find_by_name(self, name: str) -> Optional[Author]: 
        stmt = select(AuthorModel).where(AuthorModel.name == name)
        result = await self.session.execute(stmt)
        db_author = result.scalars().first()
        return AuthorMapper.to_domain(db_author)

    async def find_by_ids(self, author_ids: List[str]) -> List[Author]: 
        stmt = select(AuthorModel).where(AuthorModel.id.in_(author_ids))
        result = await self.session.execute(stmt)
        db_authors = result.scalars().all()
        return [AuthorMapper.to_domain(a) for a in db_authors]
    
    async def update(self, author: Author) -> None: 
        await self.save(author)

    async def delete(self, author_id: str) -> None: 
        stmt = delete(AuthorModel).where(AuthorModel.id == author_id)
        await self.session.execute(stmt)
        await self.session.commit()
        
        