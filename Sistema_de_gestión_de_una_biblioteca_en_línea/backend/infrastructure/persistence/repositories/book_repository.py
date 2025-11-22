from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.persistence.models import BookModel
from infrastructure.mapper_infrastructure.book_mapper import BookMapper
from domain.ports.book_repository import BookRepository
from domain.models.book import Book
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from domain.models.exceptions.business_exception import BusinessError

class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, book: Book) -> None:
        db_book = await self.session.get(BookModel, book.book_id)
        db_book_mapper = BookMapper.to_db_model(book, db_book)
        
        if not await self.session.get(BookModel, book.book_id):
            self.session.add(db_book_mapper)
            
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise BusinessError(f"Error saving book: {e}")

    async def update(self, book: Book) -> None:
        await self.save(book)

    async def find_by_id(self, book_id: str) -> Optional[Book]:
        db_book = await self.session.get(BookModel, book_id)
        return BookMapper.to_domain(db_book)

    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        stmt = select(BookModel).where(BookModel.id.in_(book_ids))
        result = await self.session.execute(stmt)
        db_books = result.scalars().all()
        return [BookMapper.to_domain(b) for b in db_books]

    async def find_by_isbn(self, isbn: ISBN) -> Optional[Book]:
        stmt = select(BookModel).where(BookModel.isbn == str(isbn))
        result = await self.session.execute(stmt)
        db_book = result.scalars().first()
        return BookMapper.to_domain(db_book)

    async def find_by_title(self, title: Title) -> Optional[Book]:
        stmt = select(BookModel).where(BookModel.title == str(title))
        result = await self.session.execute(stmt)
        db_book = result.scalars().first()
        return BookMapper.to_domain(db_book)

    async def get_all(self) -> List[Book]:
        stmt = select(BookModel)
        result = await self.session.execute(stmt)
        db_books = result.scalars().all()
        return [BookMapper.to_domain(b) for b in db_books]

    async def delete(self, book: Book) -> None:
        stmt = delete(BookModel).where(BookModel.id == book.book_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_by_author_id(self, author_id: str) -> List[Book]:
        stmt = select(BookModel).where(BookModel.author_id == author_id)
        result = await self.session.execute(stmt)
        db_books = result.scalars().all()
        return [BookMapper.to_domain(b) for b in db_books]

    async def count_by_author_id(self, author_id: str) -> int:
        stmt = select(func.count()).select_from(BookModel).where(BookModel.author_id == author_id)
        result = await self.session.execute(stmt)
        return result.scalar()
