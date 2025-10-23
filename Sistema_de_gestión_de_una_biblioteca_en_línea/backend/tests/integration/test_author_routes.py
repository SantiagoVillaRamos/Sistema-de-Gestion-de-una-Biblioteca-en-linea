from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_author_creation():
    response = client.post("/authors/", json={"name": "Author Name"})
    assert response.status_code == 201
    assert response.json()["name"] == "Author Name"

def test_get_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_author(client, author_repository):
    response = client.post(
        "/authors/",
        json={"name": "Test Author"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Author"