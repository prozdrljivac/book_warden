import pytest
import sqlite3
import tempfile
import os
from fastapi.testclient import TestClient

from main import app
from apps.books.routes import new_book_service
from apps.books.services import BookService
from apps.books.repositories import SQLiteBookRepository


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing"""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")

    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                author TEXT
            )
        """)
        conn.commit()

    yield db_path

    if os.path.exists(db_path):
        os.remove(db_path)
    os.rmdir(temp_dir)


@pytest.fixture
def test_client(temp_db):
    """Create a test client with overridden dependencies"""
    def override_book_service():
        return BookService(book_repository=SQLiteBookRepository(db_path=temp_db))
    
    app.dependency_overrides[new_book_service] = override_book_service
    
    client = TestClient(app)
    yield client
    
    # Cleanup
    app.dependency_overrides.clear()


class TestBooksAPIIntegration:
    
    def test_get_books_returns_empty_list_when_no_books(self, test_client):
        # Act
        response = test_client.get("/api/v1/books/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_create_book_with_valid_data(self, test_client):
        # Arrange
        book_data = {
            "title": "Test Book",
            "description": "Test Description",
            "author": "Test Author"
        }
        
        # Act
        response = test_client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["title"] == "Test Book"
        assert response_data["description"] == "Test Description"
        assert response_data["author"] == "Test Author"
        assert "id" in response_data
        assert isinstance(response_data["id"], int)

    def test_create_book_with_none_description(self, test_client):
        # Arrange
        book_data = {
            "title": "Test Book",
            "description": None,
            "author": "Test Author"
        }
        
        # Act
        response = test_client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["description"] == ""

    def test_create_book_with_missing_required_fields_returns_422(self, test_client):
        # Arrange
        book_data = {
            "title": "Test Book"
            # Missing author
        }
        
        # Act
        response = test_client.post("/api/v1/books/", json=book_data)
        
        # Assert
        assert response.status_code == 422

    def test_get_books_returns_created_books(self, test_client):
        # Arrange
        book1_data = {"title": "Book 1", "description": "Description 1", "author": "Author 1"}
        book2_data = {"title": "Book 2", "description": "Description 2", "author": "Author 2"}
        
        response1 = test_client.post("/api/v1/books/", json=book1_data)
        response2 = test_client.post("/api/v1/books/", json=book2_data)
        
        book1_id = response1.json()["id"]
        book2_id = response2.json()["id"]
        
        # Act
        response = test_client.get("/api/v1/books/")
        
        # Assert
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2
        
        book_ids = [book["id"] for book in books]
        assert book1_id in book_ids
        assert book2_id in book_ids

    def test_get_book_by_id_returns_existing_book(self, test_client):
        # Arrange
        book_data = {"title": "Test Book", "description": "Test Description", "author": "Test Author"}
        create_response = test_client.post("/api/v1/books/", json=book_data)
        book_id = create_response.json()["id"]
        
        # Act
        response = test_client.get(f"/api/v1/books/{book_id}")
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == book_id
        assert response_data["title"] == "Test Book"
        assert response_data["description"] == "Test Description"
        assert response_data["author"] == "Test Author"

    def test_get_book_by_nonexistent_id_returns_404(self, test_client):
        # Act
        response = test_client.get("/api/v1/books/999")
        
        # Assert
        assert response.status_code == 404

    def test_get_book_with_invalid_id_returns_422(self, test_client):
        # Act
        response = test_client.get("/api/v1/books/invalid")
        
        # Assert
        assert response.status_code == 422

    def test_update_book_with_valid_data(self, test_client):
        # Arrange
        book_data = {"title": "Original Title", "description": "Original Description", "author": "Original Author"}
        create_response = test_client.post("/api/v1/books/", json=book_data)
        book_id = create_response.json()["id"]
        
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "author": "Updated Author"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{book_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == book_id
        assert response_data["title"] == "Updated Title"
        assert response_data["description"] == "Updated Description"
        assert response_data["author"] == "Updated Author"

    def test_update_book_with_partial_data(self, test_client):
        # Arrange
        book_data = {"title": "Original Title", "description": "Original Description", "author": "Original Author"}
        create_response = test_client.post("/api/v1/books/", json=book_data)
        book_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Title"}
        
        # Act
        response = test_client.patch(f"/api/v1/books/{book_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == book_id
        assert response_data["title"] == "Updated Title"
        assert response_data["description"] == "Original Description"  # Unchanged
        assert response_data["author"] == "Original Author"  # Unchanged

    def test_update_nonexistent_book_returns_404(self, test_client):
        # Arrange
        update_data = {"title": "Updated Title"}
        
        # Act
        response = test_client.patch("/api/v1/books/999", json=update_data)
        
        # Assert
        assert response.status_code == 404

    def test_update_book_with_invalid_id_returns_422(self, test_client):
        # Arrange
        update_data = {"title": "Updated Title"}
        
        # Act
        response = test_client.patch("/api/v1/books/invalid", json=update_data)
        
        # Assert
        assert response.status_code == 422

    def test_delete_book_removes_book(self, test_client):
        # Arrange
        book_data = {"title": "Test Book", "description": "Test Description", "author": "Test Author"}
        create_response = test_client.post("/api/v1/books/", json=book_data)
        book_id = create_response.json()["id"]
        
        # Verify book exists
        get_response = test_client.get(f"/api/v1/books/{book_id}")
        assert get_response.status_code == 200
        
        # Act
        response = test_client.delete(f"/api/v1/books/{book_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify book is deleted
        get_response_after = test_client.get(f"/api/v1/books/{book_id}")
        assert get_response_after.status_code == 404

    def test_delete_nonexistent_book_returns_204(self, test_client):
        # Act
        response = test_client.delete("/api/v1/books/999")
        
        # Assert
        assert response.status_code == 204  # Should not error

    def test_delete_book_with_invalid_id_returns_422(self, test_client):
        # Act
        response = test_client.delete("/api/v1/books/invalid")
        
        # Assert
        assert response.status_code == 422
