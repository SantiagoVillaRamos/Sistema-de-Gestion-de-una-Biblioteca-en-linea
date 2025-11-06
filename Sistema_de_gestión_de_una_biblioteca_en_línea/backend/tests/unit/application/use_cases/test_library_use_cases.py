import pytest
import uuid
from application.use_cases.library.lend_book_use_case import LendBookUseCase
from application.use_cases.library.get_loan_report_use_case import GetLoanReportUseCase
from application.use_cases.library.return_book_use_case import ReturnBookUseCase
from application.dto.library_command_dto import LendBookResult, ReturnBookResponse, ReturnBookCommand, LoanReportData
from typing import List, Dict
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.book import Book
from domain.models.author import Author



@pytest.mark.asyncio
async def test_lend_book_successfully(
    use_case_dependencies, 
    lend_book_command, 
    existing_user, 
    existing_book, 
    active_loans, 
    expected_loan,
    existing_author
):
    
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_user_repo = deps["user_repo"]
    mock_book_repo = deps["book_repo"]
    mock_loan_repo = deps["loan_repo"]
    mock_author_repo = deps["author_repo"]
    mock_notification_service = deps["notification_service"]
    mock_lending_service = deps["lending_service"]

    # Estado inicial de copias
    initial_copies = existing_book.available_copies
    expected_author_names = [existing_author.name.value]
    
    # Configurar Mocks
    mock_user_repo.find_by_id.return_value = existing_user
    mock_book_repo.find_by_id.return_value = existing_book
    mock_loan_repo.find_active_loans_by_user.return_value = active_loans
    mock_author_repo.find_by_ids.return_value = [existing_author]

    # Mockear el servicio de dominio (Simulando la lógica real del LendingService)
    def mock_lend_book(user, book, active_loans):
        # Esta simulación representa la lógica DENTRO del LendingService
        book.lend()
        return expected_loan

    mock_lending_service.lend_book.side_effect = mock_lend_book
    
    # 2. Act (Ejecutar)
    use_case = LendBookUseCase(
        book_repo=mock_book_repo,
        user_repo=mock_user_repo,
        loan_repo=mock_loan_repo,
        notification_service=mock_notification_service,
        author_repos=mock_author_repo,
        lending_service=mock_lending_service
    )
    result = await use_case.execute(lend_book_command)
    
    # 3. Assert (Verificar)

    # A1. Verificar el DTO resultante
    assert isinstance(result, LendBookResult)
    assert result.user == existing_user
    assert result.book == existing_book
    assert result.loan == expected_loan
    assert result.author_names == expected_author_names
    
    # A2. Verificar la MUTACIÓN del libro (stock reducido)
    assert existing_book.available_copies == initial_copies - 1
    
    # A3. Verificar llamadas de Carga
    mock_user_repo.find_by_id.assert_called_once_with(lend_book_command.user_id)
    mock_book_repo.find_by_id.assert_called_once_with(lend_book_command.book_id)
    mock_loan_repo.find_active_loans_by_user.assert_called_once_with(existing_user.user_id)
    
    # A4. Verificar llamada al Servicio de Dominio
    mock_lending_service.lend_book.assert_called_once_with(
        existing_user, existing_book, active_loans
    )
    
    # A5. Verificar llamadas de Persistencia (el orden es importante)
    mock_book_repo.update.assert_called_once_with(existing_book) # Guarda el libro MUTADO
    mock_loan_repo.save.assert_called_once_with(expected_loan) # Guarda el nuevo préstamo
    
    # A6. Verificar llamada de Infraestructura (Notificación)
    mock_notification_service.send_loan_notification.assert_called_once_with(
        existing_user, existing_book, expected_loan
    )
    
    # A7. Verificar la obtención de nombres de autor
    mock_author_repo.find_by_ids.assert_called_once_with(existing_book.author)



@pytest.mark.asyncio
async def test_return_book_successfully(
    use_case_dependencies,
    expected_loan,          
    existing_book,         
    existing_user,          
):
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_loan_repo = deps["loan_repo"]
    mock_book_repo = deps["book_repo"]
    mock_user_repo = deps["user_repo"]
    mock_notification_service = deps["notification_service"]
    mock_returning_service = deps["returning_service"]
    
    # Datos de entrada/salida
    loan_id_to_return = expected_loan.id
    command = ReturnBookCommand(loan_id=loan_id_to_return)
    
    initial_copies = existing_book.available_copies
    expected_penalty = 0.0 # Caso exitoso sin multa

    # Configurar Mocks de Carga (Repositorios)
    mock_loan_repo.find_by_id.return_value = expected_loan
    mock_book_repo.find_by_id.return_value = existing_book
    mock_user_repo.find_by_id.return_value = existing_user

    # Mockear el Servicio de Dominio (Simula la lógica real de ReturningService)
    def mock_return_book(user, loan, book):
        """Simula que el servicio actualiza el estado del loan, llama a book.return_book() y calcula la multa."""
        # Lógica de dominio real que el servicio ejecutaría:
        loan.return_loan()  # Asumiendo que Loan tiene este método
        book.return_book()       # Aumenta el stock del libro
        return expected_penalty

    # El mock del servicio de retorno devuelve la multa esperada y ejecuta la mutación en los objetos
    mock_returning_service.return_book.side_effect = mock_return_book

    # Inicializar el Use Case
    use_case = ReturnBookUseCase(
        loan_repo=mock_loan_repo,
        book_repo=mock_book_repo,
        user_repo=mock_user_repo,
        notification_service=mock_notification_service,
        returning_service=mock_returning_service
    )

    # 2. Act (Ejecutar)
    result = await use_case.execute(command)

    # 3. Assert (Verificar)

    # A1. Verificar el DTO resultante
    # Asumiendo que ReturnBookResponse es lo que se devuelve.
    assert isinstance(result, ReturnBookResponse) 
    assert result.message == "Libro devuelto exitosamente."
    assert result.penalty_charged == expected_penalty
    
    # A2. Verificar la MUTACIÓN del libro (stock aumentado)
    # Se aumentó en 1 por la llamada a book.return_book() dentro del mock
    assert existing_book.available_copies == initial_copies + 1 
    
    # A3. Verificar llamadas de Carga
    mock_loan_repo.find_by_id.assert_called_once_with(loan_id_to_return)
    # loan.book_id y loan.user_id deben ser accedidos desde el objeto loan devuelto
    mock_book_repo.find_by_id.assert_called_once_with(expected_loan.book_id) 
    mock_user_repo.find_by_id.assert_called_once_with(expected_loan.user_id)
    
    # A4. Verificar llamada al Servicio de Dominio
    mock_returning_service.return_book.assert_called_once_with(
        existing_user, expected_loan, existing_book
    )
    
    # A5. Verificar llamadas de Persistencia (Se deben actualizar loan y book)
    mock_loan_repo.update.assert_called_once_with(expected_loan) 
    mock_book_repo.update.assert_called_once_with(existing_book)
    
    # A6. Verificar llamadas de Infraestructura (Notificaciones)
    # Notificación de retorno (siempre se envía)
    mock_notification_service.send_return_notification.assert_called_once_with(
        existing_user, existing_book
    )
    # Notificación de multa (NO se envía porque penalty=0)
    mock_notification_service.send_penalty_notification.assert_not_called()
    
    
    
@pytest.mark.asyncio
async def test_get_loan_report_successfully(
    use_case_dependencies,
    expected_loan,       # Loan 1
    overdue_loan,        # Loan 2
    existing_user,       # User 1 (para Loan 1)
    other_user,          # User 2 (para Loan 2)
    existing_book,       # Book 1 (para Loan 1)
    other_book,          # Book 2 (para Loan 2)
    existing_author,     # Author 1 (para Book 1 y Book 2)
    other_author,        # Author 2 (para Book 2 solamente)
):
    """
    Prueba que el caso de uso carga correctamente todos los préstamos y sus
    entidades relacionadas (Usuario, Libro, Autores) y ensambla el DTO final.
    """
    # 1. Arrange (Setup)
    deps = use_case_dependencies
    mock_loan_repo = deps["loan_repo"]
    mock_user_repo = deps["user_repo"]
    mock_book_repo = deps["book_repo"]
    mock_author_repo = deps["author_repo"]
    
    # 1.1 Datos simulados (Loans, Users, Books y Authors)
    all_loans: List[Loan] = [expected_loan, overdue_loan]
    all_users: List[User] = [existing_user, other_user]
    all_books: List[Book] = [existing_book, other_book]
    all_authors: List[Author] = [existing_author, other_author]
    
    # IDs de todas las entidades involucradas (Usando la lógica de IDs únicos del Use Case)
    all_user_ids = list({loan.user_id for loan in all_loans})
    all_book_ids = list({loan.book_id for loan in all_loans})
    all_author_ids_from_books = list({author_id for book in all_books for author_id in book.author})

    # 1.2 Configurar Mocks de Repositorios (Flujo de carga)
    
    # Llama 1: Cargar todos los préstamos
    mock_loan_repo.find_all.return_value = all_loans
    
    # Llamada 2: Cargar usuarios por IDs
    mock_user_repo.find_by_ids.return_value = all_users
    
    # Llamada 3: Cargar libros por IDs
    mock_book_repo.find_by_ids.return_value = all_books
    
    # Llamada 4: Cargar autores por IDs
    mock_author_repo.find_by_ids.return_value = all_authors
    
    # 1.3 Inicializar el Use Case
    use_case = GetLoanReportUseCase(
        loan_repo=mock_loan_repo,
        user_repo=mock_user_repo,
        book_repo=mock_book_repo,
        author_repo=mock_author_repo
    )

    # 2. Act (Ejecutar)
    result: List[LoanReportData] = await use_case.execute()

    # 3. Assert (Verificar)

    # A1. Verificar llamadas de Carga
    mock_loan_repo.find_all.assert_called_once()
    mock_user_repo.find_by_ids.assert_called_once_with(all_user_ids)
    mock_book_repo.find_by_ids.assert_called_once_with(all_book_ids)
    mock_author_repo.find_by_ids.assert_called_once_with(all_author_ids_from_books)

    # A2. Verificar la estructura y cantidad del resultado
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, LoanReportData) for item in result)

    # A3. Verificar el ensamblaje del primer elemento (existing_loan)
    report_data_1 = next(item for item in result if item.loan.id == expected_loan.id)
    assert report_data_1.loan == expected_loan
    assert report_data_1.user == existing_user
    assert report_data_1.book == existing_book
    # existing_book solo tiene a existing_author
    assert sorted(report_data_1.author_names) == sorted([existing_author.name.value]) 
    
    # A4. Verificar el ensamblaje del segundo elemento (overdue_loan)
    report_data_2 = next(item for item in result if item.loan.id == overdue_loan.id)
    assert report_data_2.loan == overdue_loan
    assert report_data_2.user == other_user
    assert report_data_2.book == other_book
    # other_book tiene a existing_author y other_author
    expected_authors_2 = [existing_author.name.value, other_author.name.value]
    assert sorted(report_data_2.author_names) == sorted(expected_authors_2)
    
    
    