import pytest
import uuid
from datetime import datetime
from domain.models.value_objects.due_date import DueDate
from domain.models.exceptions.business_exception import BusinessNotFoundError, BusinessConflictError
from freezegun import freeze_time 
from datetime import datetime, timedelta, timezone
from domain.models.loan import Loan

# Define una zona horaria fija para todas las pruebas
TEST_TZ = timezone(timedelta(hours=-5)) 
A_DAY = timedelta(days=1)

@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_duedate_creation_success(future_due_date_dt):
    """Prueba la creación exitosa de DueDate si la fecha está en el futuro."""
    # Act
    due_date = DueDate(future_due_date_dt)
    
    # Assert
    assert due_date.value == future_due_date_dt

@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_duedate_creation_failure_past_date(past_due_date_dt):
    """Prueba que DueDate falla si la fecha está en el pasado."""
    # Act & Assert
    with pytest.raises(BusinessNotFoundError, match="La fecha de vencimiento no puede ser en el pasado."):
        DueDate(past_due_date_dt)


# ######################################################################
# ### PRUEBAS PARA LOAN (Entidad)
# ######################################################################

# --- Pruebas de Creación (Post Init) ---

@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_loan_creation_success(valid_loan: Loan, valid_loan_date,existing_book):
    """Prueba la creación exitosa de un préstamo."""
    assert isinstance(valid_loan.due_date, DueDate)
    assert valid_loan.book_id == existing_book.book_id
    assert valid_loan.is_returned is False
    assert valid_loan.loan_date == valid_loan_date

@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_loan_creation_success_from_raw_datetime(current_time, future_due_date_dt, valid_loan_date):
    """Prueba que Loan acepta un raw datetime y lo convierte a DueDate."""
    # Act
    loan = Loan(
        id=str(uuid.uuid4()),
        book_id="BOOK-123",
        user_id="USER-456",
        loan_date=valid_loan_date,
        due_date=future_due_date_dt # Pasando raw datetime aquí
    )
    # Assert
    assert isinstance(loan.due_date, DueDate)
    assert loan.due_date.value == future_due_date_dt



@pytest.mark.parametrize("book_id, user_id", [
    ("", "USER-1"),
    ("BOOK-1", ""),
    (None, "USER-1"),
    ("BOOK-1", None),
])
@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_loan_creation_failure_missing_ids(book_id, user_id, future_due_date_dt, valid_loan_date):
    """Prueba que la creación falla si book_id o user_id están vacíos o None."""
    with pytest.raises(BusinessNotFoundError, match="El ID del libro y el ID del usuario son obligatorios."):
        Loan(
            id=str(uuid.uuid4()),
            book_id=book_id,
            user_id=user_id,
            loan_date=valid_loan_date,
            due_date=DueDate(future_due_date_dt)
        )

@freeze_time(datetime(2025, 1, 15, 10, 0, 0, tzinfo=TEST_TZ))
def test_loan_creation_failure_loan_date_after_due_date(current_time, valid_loan_date, existing_user, existing_book):
    """Prueba que la creación falla si loan_date es posterior a due_date."""
    # Arrange: loan_date es 1 hora antes de current_time. Definimos due_date 30 minutos antes de current_time.
    loan_date_late = current_time + timedelta(hours=1)
    due_date_early = DueDate(current_time + timedelta(minutes=30))

    with pytest.raises(BusinessNotFoundError, match="La fecha de préstamo no puede ser posterior a la fecha de vencimiento."):
        Loan(
            id=str(uuid.uuid4()),
            book_id=existing_book.book_id,
            user_id=existing_user.user_id,
            loan_date=loan_date_late,
            due_date=due_date_early
        )

# --- Pruebas de Comportamiento (Métodos) ---

def test_return_loan_success(valid_loan: Loan):
    """Prueba el retorno exitoso de un préstamo."""
    # Act
    valid_loan.return_loan()
    
    # Assert
    assert valid_loan.is_returned is True

def test_return_loan_failure_already_returned(valid_loan: Loan):
    """Prueba que el retorno falla si el préstamo ya fue devuelto."""
    # Arrange: Devolverlo primero
    valid_loan.return_loan()
    
    # Act & Assert
    with pytest.raises(BusinessConflictError, match="El préstamo ya fue devuelto."):
        valid_loan.return_loan()

# --- Pruebas de Overdue (Vencimiento) ---

@freeze_time(datetime(2025, 1, 16, 10, 0, 1, tzinfo=TEST_TZ)) # Congelamos el tiempo 1 segundo DESPUÉS del vencimiento (16/01 10:00:00)
def test_is_overdue_true_not_returned(valid_loan: Loan):
    """Prueba que un préstamo NO devuelto y VENCIDO es Overdue."""
    # Arrange: valid_loan due_date es 2025-01-16 10:00:00.
    assert valid_loan.is_returned is False
    
    # Act & Assert
    assert valid_loan.is_overdue() is True

@freeze_time(datetime(2025, 1, 16, 10, 0, 1, tzinfo=TEST_TZ))
def test_is_overdue_false_returned(valid_loan: Loan):
    """Prueba que un préstamo DEVUELTO, aunque esté cronológicamente vencido, NO es Overdue."""
    # Arrange
    valid_loan.return_loan()
    
    # Act & Assert
    assert valid_loan.is_overdue() is False

@freeze_time(datetime(2025, 1, 15, 20, 0, 0, tzinfo=TEST_TZ)) # Congelamos el tiempo ANTES del vencimiento (16/01 10:00:00)
def test_is_overdue_false_not_due_yet(valid_loan: Loan):
    """Prueba que un préstamo NO devuelto que aún NO ha vencido NO es Overdue."""
    # Arrange
    assert valid_loan.is_returned is False
    
    # Act & Assert
    assert valid_loan.is_overdue() is False