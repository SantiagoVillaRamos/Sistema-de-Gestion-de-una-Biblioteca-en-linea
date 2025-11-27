import pytest
from fastapi.testclient import TestClient
from main import app

# 🔒 SECURITY TEST SUITE
# Verifies that input validation and sanitization mechanisms are working correctly.

class TestSecurityPayloads:
    
    # =========================================================================
    # 1. XSS PREVENTION TESTS
    # =========================================================================
    
    def test_xss_in_user_name(self, client: TestClient):
        """Verify that XSS payloads in user name are rejected."""
        payload = {
            "name": "<script>alert('XSS')</script>",
            "email": "xss_test@example.com",
            "password": "Password123!",
            "user_type": "general"
        }
        response = client.post("/users/", json=payload)
        
        # Expecting 400 Bad Request due to validation failure
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "html tags" in detail or "invalid character" in detail

    def test_xss_in_book_title(self, client: TestClient, admin_user_token: str):
        """Verify that XSS payloads in book title are rejected."""
        payload = {
            "title": "Book with <img src=x onerror=alert(1)>",
            "isbn": "978-0-123-45678-9",
            "description": "Valid description",
            "available_copies": 5,
            "author": ["some-author-id"]
        }
        
        headers = {"Authorization": f"Bearer {admin_user_token}"}
        response = client.post("/books/", json=payload, headers=headers)
        
        # Expecting 400 Bad Request due to validation failure
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "html tags" in detail or "invalid character" in detail

    # =========================================================================
    # 2. SQL INJECTION PREVENTION TESTS
    # =========================================================================

    def test_sql_injection_in_book_title(self, client: TestClient, admin_user_token: str):
        """Verify that SQL injection patterns are blocked."""
        payload = {
            "title": "'; DROP TABLE books; --",
            "isbn": "978-0-123-45678-9",
            "description": "SQL Injection Test",
            "available_copies": 5,
            "author": ["some-author-id"]
        }
        
        headers = {"Authorization": f"Bearer {admin_user_token}"}
        response = client.post("/books/", json=payload, headers=headers)
        
        # Expecting 400 Bad Request due to validation failure
        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "potentially dangerous" in detail or "invalid character" in detail

    # =========================================================================
    # 3. INPUT VALIDATION LIMITS
    # =========================================================================

    def test_long_user_name(self, client: TestClient):
        """Verify that names exceeding max length are rejected."""
        long_name = "A" * 101 # Max is 100
        payload = {
            "name": long_name,
            "email": "long_name@example.com",
            "password": "Password123!",
            "user_type": "general"
        }
        response = client.post("/users/", json=payload)
        assert response.status_code == 422 # Pydantic validation error

    def test_invalid_isbn_format(self, client: TestClient, admin_user_token: str):
        """Verify that invalid ISBN format is rejected."""
        payload = {
            "title": "Valid Title",
            "isbn": "12345", # Too short
            "description": "Valid description",
            "available_copies": 5,
            "author": ["some-author-id"]
        }
        
        headers = {"Authorization": f"Bearer {admin_user_token}"}
        response = client.post("/books/", json=payload, headers=headers)
        
        assert response.status_code == 422 # Pydantic validation error
