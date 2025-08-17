import pytest

from apps.books.services import (
    BookService,
    InvalidBookIdValueError,
    InvalidBookTitleValueError,
    InvalidBookDescriptionValueError,
    InvalidBookAuthorValueError,
)

from tests.config import mock_book_repository

def test_book_service_creation(mock_book_repository):
    service = BookService(book_repository = mock_book_repository)
    assert service.book_repository == mock_book_repository

def test_book_with_valid_id(mock_book_repository):
    # Arrange
    service = BookService(book_repository = mock_book_repository)

    # Act
    service.book(id=1)

    # Assert
    mock_book_repository.book.assert_called_once_with(id=1)

def test_book_with_invalid_id_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository = mock_book_repository)
    invalid_ids = [-1, "string", None, 3.14, True, False]

    # Act and Assert
    for invalid_id in invalid_ids:
        with pytest.raises(InvalidBookIdValueError, match="Book ID needs to be a non negative integer"):
            service.book(id=invalid_id)

def test_new_book_with_valid_title_description_author(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    valid_book_entries = [
        {"title": "Title 1", "description": "Description 1", "author": "Author 1"},
        {"title": "Title 1", "description": None, "author": "Author 1"},
    ]

    # Act
    for valid_entry in valid_book_entries:
        service.new_book(
            title=valid_entry["title"],
            description=valid_entry["description"],
            author=valid_entry["author"]
        )

    # Assert
    mock_book_repository.create_book.call_count == len(valid_book_entries)

def test_new_book_with_invalid_title(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_titles = [3, True, False, [0, 1, 2], {"test": 1}, 3,14, None]

    # Act & Assert
    for invalid_title in invalid_titles:
        with pytest.raises(InvalidBookTitleValueError, match="Book title needs to be text"):
            service.new_book(
                title=invalid_title,
                description="Test Description",
                author="Test Author"
            )

def test_new_book_with_invalid_description(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_descriptions = [3, True, False, [0, 1, 2], {"test": 1}, 3.14]

    # Act & Assert
    for invalid_description in invalid_descriptions:
        with pytest.raises(InvalidBookDescriptionValueError, match="Book description needs to be text"):
            service.new_book(
                title="Test Title",
                description=invalid_description,
                author="Test Author"
            )

def test_new_book_with_invalid_author(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_authors = [3, True, False, [0, 1, 2], {"test": 1}, 3.14, None]

    # Act & Assert
    for invalid_author in invalid_authors:
        with pytest.raises(InvalidBookAuthorValueError, match="Book author needs to be text"):
            service.new_book(
                title="Test Title",
                description="Test Description",
                author=invalid_author
            )

def test_all_books(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)

    # Act
    service.all_books()

    # Assert
    mock_book_repository.all_books.assert_called_once()

def test_update_book_with_valid_id_and_fields(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)

    # Act
    service.update_book(id=1, title="New Title", description="New Description", author="New Author")

    # Assert
    mock_book_repository.update_book.assert_called_once_with(
        id=1, title="New Title", description="New Description", author="New Author"
    )

def test_update_book_with_valid_id_and_partial_fields(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)

    # Act
    service.update_book(id=1, title="New Title", description=None, author=None)

    # Assert
    mock_book_repository.update_book.assert_called_once_with(
        id=1, title="New Title", description=None, author=None
    )

def test_update_book_with_invalid_id_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_ids = [-1, "string", None, 3.14, True, False]

    # Act and Assert
    for invalid_id in invalid_ids:
        with pytest.raises(InvalidBookIdValueError, match="Book ID needs to be a non negative integer"):
            service.update_book(id=invalid_id, title="Title", description="Description", author="Author")

def test_update_book_with_invalid_title_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_titles = [3, True, False, [0, 1, 2], {"test": 1}, 3.14]

    # Act & Assert
    for invalid_title in invalid_titles:
        with pytest.raises(InvalidBookTitleValueError, match="Book title needs to be text"):
            service.update_book(
                id=1,
                title=invalid_title,
                description="Test Description",
                author="Test Author"
            )

def test_update_book_with_invalid_description_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_descriptions = [3, True, False, [0, 1, 2], {"test": 1}, 3.14]

    # Act & Assert
    for invalid_description in invalid_descriptions:
        with pytest.raises(InvalidBookDescriptionValueError, match="Book description needs to be text"):
            service.update_book(
                id=1,
                title="Test Title",
                description=invalid_description,
                author="Test Author"
            )

def test_update_book_with_invalid_author_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_authors = [3, True, False, [0, 1, 2], {"test": 1}, 3.14]

    # Act & Assert
    for invalid_author in invalid_authors:
        with pytest.raises(InvalidBookAuthorValueError, match="Book author needs to be text"):
            service.update_book(
                id=1,
                title="Test Title",
                description="Test Description",
                author=invalid_author
            )

def test_remove_book_with_valid_id(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)

    # Act
    service.remove_book(id=1)

    # Assert
    mock_book_repository.delete_book.assert_called_once_with(id=1)

def test_remove_book_with_invalid_id_raises_error(mock_book_repository):
    # Arrange
    service = BookService(book_repository=mock_book_repository)
    invalid_ids = [-1, "string", None, 3.14, True, False]

    # Act and Assert
    for invalid_id in invalid_ids:
        with pytest.raises(InvalidBookIdValueError, match="Book ID needs to be a non negative integer"):
            service.remove_book(id=invalid_id)
