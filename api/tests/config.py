import pytest
from unittest.mock import Mock

from apps.books.repositories import BookRepository


@pytest.fixture
def mock_book_repository():
    return Mock(spec=BookRepository)
