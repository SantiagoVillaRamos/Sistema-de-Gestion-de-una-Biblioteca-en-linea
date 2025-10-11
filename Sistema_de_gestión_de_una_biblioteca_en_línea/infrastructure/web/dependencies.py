from infrastructure.persistence.in_memory.book_in_memory_repository import BookInMemoryRepository
from infrastructure.persistence.in_memory.user_in_memory_repository import UserInMemoryRepository
from infrastructure.persistence.in_memory.loan_in_memory_repository import LoanInMemoryRepository
from application.facade.facade_library import LibraryFacade
from infrastructure.services.email_notification_service import EmailNotificationService
from application.facade.facade_user import UserFacade
from application.facade.facade_book import BookFacade

# Instancias de repositorios (simulando un Singleton)
class Repositories:
    
    book_repo = BookInMemoryRepository()
    user_repo = UserInMemoryRepository()
    loan_repo = LoanInMemoryRepository()
    notification_service = EmailNotificationService()
    
repos = Repositories()

def get_library_facade() -> LibraryFacade:
    return LibraryFacade(repos.book_repo, repos.user_repo, repos.loan_repo, repos.notification_service)

def get_user_facade() -> UserFacade:
    return UserFacade(repos.book_repo, repos.user_repo, repos.loan_repo)

def get_book_facade() -> BookFacade:
    return BookFacade(repos.book_repo)
