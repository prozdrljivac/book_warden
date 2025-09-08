import pytest
import sqlite3
import tempfile
import os

from apps.books.repositories import SQLiteBookRepository

@pytest.fixture
def temp_db():
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
def repository(temp_db):
    """Create a repository instance with temporary database"""
    return SQLiteBookRepository(db_path=temp_db)


class TestSQLiteBookRepositoryIntegration:
    def test_create_book_stores_in_database(self, repository, temp_db):
        # Act
        book = repository.create_book(
            title="Test Title",
            description="Test Description", 
            author="Test Author"
        )

        # Assert
        assert book.id is not None
        assert book.title == "Test Title"
        assert book.description == "Test Description"
        assert book.author == "Test Author"

        # Verify directly in database
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM books WHERE id = ?", (book.id,))
            db_book = result.fetchone()
            assert db_book is not None
            assert db_book[1] == "Test Title"
            assert db_book[2] == "Test Description"
            assert db_book[3] == "Test Author"

    def test_create_book_with_none_description(self, repository):
        # Act
        book = repository.create_book(
            title="Test Title",
            description=None,
            author="Test Author"
        )

        # Assert
        assert book.description == ""

    def test_all_books_returns_empty_list_when_no_books(self, repository):
        # Act
        books = repository.all_books()

        # Assert
        assert books == []

    def test_all_books_returns_all_stored_books(self, repository):
        # Arrange
        book1 = repository.create_book("Title 1", "Description 1", "Author 1")
        book2 = repository.create_book("Title 2", "Description 2", "Author 2")

        # Act
        books = repository.all_books()

        # Assert
        assert len(books) == 2
        book_ids = [book.id for book in books]
        assert book1.id in book_ids
        assert book2.id in book_ids

    def test_book_returns_existing_book(self, repository):
        # Arrange
        created_book = repository.create_book("Test Title", "Test Description", "Test Author")

        # Act
        retrieved_book = repository.book(created_book.id)

        # Assert
        assert retrieved_book is not None
        assert retrieved_book.id == created_book.id
        assert retrieved_book.title == created_book.title
        assert retrieved_book.description == created_book.description
        assert retrieved_book.author == created_book.author

    def test_book_returns_none_for_nonexistent_id(self, repository):
        # Act
        book = repository.book(999)

        # Assert
        assert book is None

    def test_update_book_updates_all_fields(self, repository):
        # Arrange
        created_book = repository.create_book("Original Title", "Original Description", "Original Author")

        # Act
        updated_book = repository.update_book(
            id=created_book.id,
            title="Updated Title",
            description="Updated Description", 
            author="Updated Author"
        )

        # Assert
        assert updated_book is not None
        assert updated_book.id == created_book.id
        assert updated_book.title == "Updated Title"
        assert updated_book.description == "Updated Description"
        assert updated_book.author == "Updated Author"

    def test_update_book_updates_partial_fields(self, repository):
        # Arrange
        created_book = repository.create_book("Original Title", "Original Description", "Original Author")

        # Act
        updated_book = repository.update_book(
            id=created_book.id,
            title="Updated Title",
            description=None,
            author=None
        )

        # Assert
        assert updated_book is not None
        assert updated_book.id == created_book.id
        assert updated_book.title == "Updated Title"
        assert updated_book.description == "Original Description"  # Unchanged
        assert updated_book.author == "Original Author"  # Unchanged

    def test_update_book_returns_none_for_nonexistent_id(self, repository):
        # Act
        result = repository.update_book(
            id=999,
            title="New Title", 
            description="New Description",
            author="New Author"
        )

        # Assert
        assert result is None

    def test_update_book_returns_none_when_no_fields_to_update(self, repository):
        # Arrange
        created_book = repository.create_book("Test Title", "Test Description", "Test Author")

        # Act
        result = repository.update_book(
            id=created_book.id,
            title=None,
            description=None,
            author=None
        )

        # Assert
        assert result is None

    def test_delete_book_removes_from_database(self, repository, temp_db):
        # Arrange
        created_book = repository.create_book("Test Title", "Test Description", "Test Author")

        # Verify book exists
        assert repository.book(created_book.id) is not None

        # Act
        repository.delete_book(created_book.id)

        # Assert
        assert repository.book(created_book.id) is None

        # Verify directly in database
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM books WHERE id = ?", (created_book.id,))
            db_book = result.fetchone()
            assert db_book is None

    def test_delete_book_with_nonexistent_id_does_not_error(self, repository):
        # Act & Assert (should not raise exception)
        repository.delete_book(999)
