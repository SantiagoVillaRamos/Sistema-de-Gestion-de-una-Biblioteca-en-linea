
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
    print(loan_info)
    assert "loan_id" in loan_info
    
    



