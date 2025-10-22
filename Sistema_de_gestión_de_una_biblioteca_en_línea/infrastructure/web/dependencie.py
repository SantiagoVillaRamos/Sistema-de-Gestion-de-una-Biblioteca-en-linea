from infrastructure.persistence.in_memory.book_in_memory_repository import BookInMemoryRepository
from infrastructure.persistence.in_memory.user_in_memory_repository import UserInMemoryRepository
from infrastructure.persistence.in_memory.loan_in_memory_repository import LoanInMemoryRepository
from infrastructure.persistence.in_memory.author_in_memory_repository import AuthorInMemoryRepository
from application.facade.facade_library import LibraryFacade
from infrastructure.services.email_notification_service import EmailNotificationService
from infrastructure.services.passlib_password_service import PasslibPasswordService
from infrastructure.services.jwt_auth_service import JwtAuthService
from application.facade.facade_user import UserFacade
from application.facade.facade_book import FacadeBook
from application.facade.facade_author import AuthorFacade
from application.facade.facade_auth import AuthFacade
from application.use_cases.author.create_author_use_case import CreateAuthorUseCase
from application.use_cases.author.get_all_authors_use_case import GetAllAuthorsUseCase
from application.use_cases.author.get_author_by_id_use_case import GetAuthorByIdUseCase
from application.use_cases.author.update_author_use_case import UpdateAuthorUseCase
from application.use_cases.author.delete_author_use_case import DeleteAuthorUseCase
from application.use_cases.user.login_user_use_case import LoginUserUseCase
from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.use_cases.user.get_user_use_case import GetUserUseCase
from application.use_cases.user.get_all_users_use_case import GetAllUsersUseCase
from application.use_cases.user.update_current_user_use_case import UpdateCurrentUserUseCase
from application.use_cases.user.get_user_loan_history_use_case import GetUserLoanHistoryUseCase
from application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.use_cases.book.update_book_use_case import UpdateBookUseCase
from application.use_cases.book.get_all_books_use_case import GetAllBooksUseCase
from application.use_cases.book.get_book_by_id_use_case import GetBookByIdUseCase
from application.use_cases.book.delete_book_use_case import DeleteBookUseCase
from application.use_cases.library.lend_book_use_case import LendBookUseCase
from application.use_cases.library.return_book_use_case import ReturnBookUseCase
from application.use_cases.library.get_loan_report_use_case import GetLoanReportUseCase
from domain.models.factory.userFactory import UserFactory
from domain.services.UpdateCurrentService import UserUpdaterService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from domain.models.user import User

# Instancias de repositorios (simulando un Singleton)
class Repositories:
    
    book_repo = BookInMemoryRepository()
    user_repo = UserInMemoryRepository()
    loan_repo = LoanInMemoryRepository()
    author_repo = AuthorInMemoryRepository()
    notification_service = EmailNotificationService()
    password_service = PasslibPasswordService()
    user_updated_service = UserUpdaterService(password_service=password_service)
    
    auth_service = JwtAuthService(secret_key="a_very_secret_key")
    
repos = Repositories()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_library_facade() -> LibraryFacade:
    
    lend_book_use_case = LendBookUseCase(
        book_repo=repos.book_repo,
        user_repo=repos.user_repo,
        loan_repo=repos.loan_repo,
        notification_service=repos.notification_service,
        author_repos=repos.author_repo
    )
    return_book_use_case = ReturnBookUseCase(
        loan_repo=repos.loan_repo,
        book_repo=repos.book_repo,
        user_repo=repos.user_repo,
        notification_service=repos.notification_service
    )
    get_loan_report_use_case = GetLoanReportUseCase(
        loan_repo=repos.loan_repo,
        user_repo=repos.user_repo,
        book_repo=repos.book_repo,
        author_repo=repos.author_repo
    )
    
    return LibraryFacade(
        lend_book_use_case=lend_book_use_case,
        return_book_use_case=return_book_use_case,
        get_loan_report_use_case=get_loan_report_use_case
    )


def get_user_facade() -> UserFacade:
    user_factory = UserFactory(
        password_service=repos.password_service
    )
    create_user_use_case = CreateUserUseCase(
        user_repository=repos.user_repo, 
        user_factory=user_factory
    )
    get_user_use_case = GetUserUseCase(
        user_repo=repos.user_repo, 
        loan_repo=repos.loan_repo, 
        book_repo=repos.book_repo, 
        author_repository=repos.author_repo
    )
    all_users_use_case = GetAllUsersUseCase(
        user_repository=repos.user_repo
    )
    update_current_user_uc = UpdateCurrentUserUseCase(
        user_repo=repos.user_repo,
        user_updater_service=repos.user_updated_service
    )
    get_user_loan_history_use_case = GetUserLoanHistoryUseCase(
        user_repo=repos.user_repo,
        loan_repo=repos.loan_repo,
        book_repo=repos.book_repo,
        author_repo=repos.author_repo
    )
    delete_user_use_case = DeleteUserUseCase(
        user_repo=repos.user_repo
    )
    return UserFacade(
        create_user_use_case, 
        get_user_use_case,
        all_users_use_case, 
        update_current_user_uc, 
        get_user_loan_history_use_case,
        delete_user_use_case
    )



def get_book_facade() -> FacadeBook:
    create_book_use_case = CreateBookUseCase(
        book_repository=repos.book_repo, 
        author_repository=repos.author_repo
    )
    update_book_use_case = UpdateBookUseCase(
        book_repository=repos.book_repo, 
        author_repository=repos.author_repo
    )
    get_all_books_use_case = GetAllBooksUseCase(
        book_repository=repos.book_repo, 
        author_repository=repos.author_repo
    )
    get_book_by_id_use_case = GetBookByIdUseCase(
        book_repository=repos.book_repo, 
        author_repository=repos.author_repo
    )
    delete_book_use_case = DeleteBookUseCase(book_repository=repos.book_repo)
    
    return FacadeBook(
        create_book_use_case=create_book_use_case,
        update_book_use_case=update_book_use_case,
        get_all_books_use_case=get_all_books_use_case,
        get_book_by_id_use_case=get_book_by_id_use_case,
        delete_book_use_case=delete_book_use_case
    )


def get_author_facade() -> AuthorFacade:
    create_author_use_case = CreateAuthorUseCase(
        author_repository=repos.author_repo
    )
    get_all_authors_use_case = GetAllAuthorsUseCase(
        author_repository=repos.author_repo
    )
    get_author_by_id_use_case = GetAuthorByIdUseCase(
        author_repository=repos.author_repo,
        book_repository=repos.book_repo
    )
    update_data_author = UpdateAuthorUseCase(
        author_repository=repos.author_repo
    )
    delete_author_data = DeleteAuthorUseCase(
        author_repository=repos.author_repo, 
        book_repository=repos.book_repo
    )
    
    return AuthorFacade(
        create_use_case = create_author_use_case,
        get_all_use_case=get_all_authors_use_case,
        get_by_id_use_case=get_author_by_id_use_case,
        update_use_case=update_data_author,
        delete_author_data=delete_author_data
    )




def get_auth_facade() -> AuthFacade:
    login_use_case = LoginUserUseCase(
        user_repository=repos.user_repo,
        password_service=repos.password_service,
        auth_service=repos.auth_service
    )
    return AuthFacade(login_use_case)





async def get_current_user(token: Annotated[str | None, Depends(oauth2_scheme)]) -> User:
    if token is None:
        # This happens when auto_error=False and no token is provided.
        # We explicitly raise the 401 error that would have been raised automatically.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = repos.auth_service.validate_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e: # Catches validation errors from auth_service
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await repos.user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_optional_current_user(token: Annotated[str | None, Depends(oauth2_scheme)] = None) -> User | None:
    if token is None:
        return None
    try:
        return await get_current_user(token)
    except HTTPException:
        return None

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_user)]):
        if not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operacion no Permitida"
            )
