from abc import ABC, abstractmethod
from domain.models.user import User
from domain.models.loan import Loan
from domain.models.book import Book

class NotificationService(ABC):
    """
    Puerto (Interfaz) que define el contrato para un servicio de notificaciones.
    La capa de aplicación depende de esta abstracción, no de una implementación concreta.
    """

    @abstractmethod
    async def send_loan_notification(self, user: User, book: Book, loan: Loan) -> None:
        """Envía una notificación al usuario sobre un nuevo préstamo."""
        pass

    @abstractmethod
    async def send_return_notification(self, user: User, book: Book) -> None:
        """Envía una notificación al usuario sobre la devolución de un libro."""
        pass

    @abstractmethod
    async def send_penalty_notification(self, user: User, book: Book, penalty: float) -> None:
        """Envía una notificación al usuario sobre una multa aplicada."""
        pass