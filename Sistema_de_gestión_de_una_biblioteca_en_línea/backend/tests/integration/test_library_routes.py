
from fastapi.testclient import TestClient
from tests.utils.auth_test_utils import BASE_URL_LOAN


def test_lend_book_successful(client: TestClient, loan_prerequisites: dict):
    """
    Prueba de prestar un libro de forma exitosa.
    Utiliza el fixture loan_prerequisites para el setup completo.
    """
    
    # 1. Extraer los datos esenciales del fixture
    user_id = loan_prerequisites["borrower_id"]
    token = loan_prerequisites["borrower_token"]
    book_id = loan_prerequisites["book_id"]
    
    # 2. Datos de la solicitud de préstamo
    loan_request = {
        "user_id": user_id,
        "book_id": book_id
    }
    
    # 3. Ejecutar la solicitud POST
    response = client.post(
        f"{BASE_URL_LOAN}/lend", 
        json=loan_request, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 4. Aserciones
    assert response.status_code == 201, f"Fallo al prestar un libro: {response.status_code} - {response.text}" 
    
    loan_info = response.json()

    assert "loan_id" in loan_info
    assert "message" in loan_info
    assert "loan_date" in loan_info
    assert "due_date" in loan_info
    assert "user" in loan_info
    assert "book" in loan_info
    
    assert isinstance(loan_info["loan_id"], str)
    assert isinstance(loan_info["message"], str)
    assert isinstance(loan_info["loan_date"], str)
    assert isinstance(loan_info["due_date"], str)
    assert isinstance(loan_info["user"], dict)
    assert isinstance(loan_info["book"], dict)
    


def test_return_book_successful(client:TestClient, loan_prerequisites: dict):
    
    # 1. Extraer los datos esenciales del fixture
    user_id = loan_prerequisites["borrower_id"]
    token = loan_prerequisites["borrower_token"]
    book_id = loan_prerequisites["book_id"]
    
    # 2. Datos de la solicitud de préstamo
    loan_request = {
        "user_id": user_id,
        "book_id": book_id
    }
    
    # 3. Ejecutar la solicitud POST
    response = client.post(
        f"{BASE_URL_LOAN}/lend", 
        json=loan_request, 
        headers={"Authorization": f"Bearer {token}"}
    )
    loan_data = response.json()
    loan_id = loan_data["loan_id"]
    
    return_request = {
        "loan_id": loan_id
    }
    
    returned_book = client.post(
        f"{BASE_URL_LOAN}/return",
        json=return_request,
        headers={"Authorization": f"Bearer {token}"}
    )

    response_json = returned_book.json()
    
    assert "message" in response_json
    assert "penalty_charged" in response_json
    assert isinstance(response_json["message"], str)
    assert isinstance(response_json["penalty_charged"], float)
    assert "Libro devuelto exitosamente." in response_json["message"]
    
    
def test_get_loan_report(client: TestClient, loan_prerequisites: dict):
    
    # 1. Extraer los datos esenciales del fixture
    user_id = loan_prerequisites["borrower_id"]
    token = loan_prerequisites["borrower_token"]
    book_id = loan_prerequisites["book_id"]
    
    # 2. Datos de la solicitud de préstamo
    loan_request = {
        "user_id": user_id,
        "book_id": book_id
    }
    
    # 3. Ejecutar la solicitud POST
    response = client.post(
        f"{BASE_URL_LOAN}/lend", 
        json=loan_request, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response_report = client.get(
        f"{BASE_URL_LOAN}/report", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response_get_loan_report = response_report.json()
    
    assert isinstance(response_get_loan_report, list)
    
    assert all("loan_id" in loan_id for loan_id in response_get_loan_report)
    assert all("loan_date" in loan_date for loan_date in response_get_loan_report)
    assert all("due_date" in due_date for due_date in response_get_loan_report)
    assert all("user_id" in user_id for user_id in response_get_loan_report)
    assert all("user_name" in user_name for user_name in response_get_loan_report)
    assert all("user_email" in user_email for user_email in response_get_loan_report)
    assert all("book_id" in book_id for book_id in response_get_loan_report)
    assert all("book_title" in book_title for book_title in response_get_loan_report)
    assert all("book_description" in book_description for book_description in response_get_loan_report)
    assert all("book_authors" in book_authors for book_authors in response_get_loan_report)
    
    assert all(isinstance(loan_id["loan_id"], str) for loan_id in response_get_loan_report)
    assert all(isinstance(loan_date["loan_date"], str) for loan_date in response_get_loan_report)
    assert all(isinstance(due_date["due_date"], str) for due_date in response_get_loan_report)
    assert all(isinstance(user_id["user_id"], str) for user_id in response_get_loan_report)
    assert all(isinstance(user_name["user_name"], str) for user_name in response_get_loan_report)
    assert all(isinstance(user_email["user_email"], str) for user_email in response_get_loan_report)
    assert all(isinstance(book_id["book_id"], str) for book_id in response_get_loan_report)
    assert all(isinstance(book_title["book_title"], str) for book_title in response_get_loan_report)
    assert all(isinstance(book_description["book_description"], str) for book_description in response_get_loan_report)
    assert all(isinstance(book_authors["book_authors"], list) for book_authors in response_get_loan_report)