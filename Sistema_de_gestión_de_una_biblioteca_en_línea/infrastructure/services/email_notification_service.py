from application.ports.notification_service import NotificationService
from domain.models.user import User
from domain.models.loan import Loan
from domain.models.book import Book


class EmailNotificationService(NotificationService):
    """
    Adaptador que implementa el puerto de notificaciones para enviar correos electrónicos.
    En un sistema real, aquí iría la lógica para conectarse a un servidor SMTP
    o a una API de terceros como SendGrid, Mailgun, etc.
    """

    async def send_loan_notification(self, user: User, book: Book, loan: Loan) -> None:
        subject = f"Confirmación de préstamo: {book.title.value}"
        body = (
            f"Hola {user.name},\n\n"
            f"Te confirmamos el préstamo del libro '{book.title.value}'.\n"
            f"La fecha de devolución es el {loan.due_date.value.strftime('%d-%m-%Y')}.\n\n"
            "¡Disfruta de tu lectura!"
        )
        
        print(f"\n--- SIMULANDO ENVÍO DE CORREO ---")
        print(f"Para: {user.email.address}")
        print(f"Asunto: {subject}")
        print(f"Cuerpo:\n{body}")
        print(f"---------------------------------\n")
        # Aquí iría el código real de envío de correo:
        # import smtplib
        # with smtplib.SMTP('smtp.example.com') as server:
        #     server.sendmail('biblioteca@example.com', user.email.address, f"Subject: {subject}\n\n{body}")

    async def send_return_notification(self, user: User, book: Book) -> None:
        message = (
            f"Hola {user.name}, "
            f"confirmamos la devolución del libro '{book.title.value}'. ¡Gracias!"
        )
        
        print(f"\n--- SIMULando ENVÍO DE SMS ---")
        # En un caso real, necesitaríamos el número de teléfono del usuario.
        # print(f"Para: {user.phone_number}") 
        print(f"Mensaje: {message}")
        print(f"----------------------------\n")

    async def send_penalty_notification(self, user: User, book: Book, penalty: float) -> None:
        message = (
            f"Hola {user.name}, se ha aplicado una multa de ${penalty:.2f} "
            f"por la devolución tardía del libro '{book.title.value}'."
        )
        
        print(f"\n--- SIMULANDO ENVÍO DE SMS (MULTA) ---")
        # En un caso real, necesitaríamos el número de teléfono del usuario.
        # print(f"Para: {user.phone_number}") 
        print(f"Mensaje: {message}")
        print(f"-------------------------------------\n")