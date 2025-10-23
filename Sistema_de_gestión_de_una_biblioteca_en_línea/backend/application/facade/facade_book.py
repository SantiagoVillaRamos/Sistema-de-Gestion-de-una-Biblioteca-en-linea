from typing import List
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.use_cases.book.update_book_use_case import UpdateBookUseCase
from application.use_cases.book.get_all_books_use_case import GetAllBooksUseCase
from application.use_cases.book.get_book_by_id_use_case import GetBookByIdUseCase
from application.use_cases.book.delete_book_use_case import DeleteBookUseCase
from application.dto.book_command_dto import CreateBookCommand, UpdateBookDTOCommand
from domain.models.book import Book

class FacadeBook:
    def __init__(
        self,
        create_book_use_case: CreateBookUseCase,
        update_book_use_case: UpdateBookUseCase,
        get_all_books_use_case: GetAllBooksUseCase,
        get_book_by_id_use_case: GetBookByIdUseCase,
        delete_book_use_case: DeleteBookUseCase,
    ):
        self.create_book_use_case = create_book_use_case
        self.update_book_use_case = update_book_use_case
        self.get_all_books_use_case = get_all_books_use_case
        self.get_book_by_id_use_case = get_book_by_id_use_case
        self.delete_book_use_case = delete_book_use_case

    async def create_book(self, command: CreateBookCommand) -> Book:
        return await self.create_book_use_case.execute(command)

    async def update_book(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Book:
        return await self.update_book_use_case.execute(book_id, update_dto)

    async def get_all_books(self) -> List[Book]:
        return await self.get_all_books_use_case.execute()

    async def get_book_by_id(self, book_id: str) -> Book | None:
        return await self.get_book_by_id_use_case.execute(book_id)

    async def delete_book(self, book_id: str) -> None:
        await self.delete_book_use_case.execute(book_id)