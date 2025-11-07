from typing import List

from application.ports.book.create_book import CreaterBook
from application.ports.book.delete_book import DeleteBook
from application.ports.book.get_all_books import GetAllBooks
from application.ports.book.get_book_by_id import GetBookById
from application.ports.book.update_book import UpdateBook

from application.dto.book_command_dto import CreateBookCommand, UpdateBookDTOCommand
from domain.models.book import Book

class FacadeBook:
    def __init__(
        self,
        create_book_use_case: CreaterBook,
        update_book_use_case: UpdateBook,
        get_all_books_use_case: GetAllBooks,
        get_book_by_id_use_case: GetBookById,
        delete_book_use_case: DeleteBook,
    ):
        self.create_book_use_case = create_book_use_case
        self.update_book_use_case = update_book_use_case
        self.get_all_books_use_case = get_all_books_use_case
        self.get_book_by_id_use_case = get_book_by_id_use_case
        self.delete_book_use_case = delete_book_use_case

    async def create_book(self, command: CreateBookCommand) -> Book:
        return await self.create_book_use_case.create_book(command)

    async def update_book(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Book:
        return await self.update_book_use_case.update_book(book_id, update_dto)

    async def get_all_books(self) -> List[Book]:
        return await self.get_all_books_use_case.get_all_books()

    async def get_book_by_id(self, book_id: str) -> Book | None:
        return await self.get_book_by_id_use_case.get_book_by_id(book_id)

    async def delete_book(self, book_id: str) -> None:
        await self.delete_book_use_case.delete_book(book_id)