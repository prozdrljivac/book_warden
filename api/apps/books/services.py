from typing import List, Optional

from apps.books.models import BookModel
from apps.books.repositories import BookRepository
from apps.validators import is_non_negative_strict_integer


class InvalidBookIdValueError(ValueError):
    """Raised when book ID is invalid"""
    pass

class InvalidBookTitleValueError(ValueError):
    """Raised when book title is not a string"""
    pass

class InvalidBookDescriptionValueError(ValueError):
    """Raised when book description is not a string"""
    pass

class InvalidBookAuthorValueError(ValueError):
    """Raised when book author is not a string"""
    pass

class BookService():
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def all_books(self) -> List[BookModel]:
        return self.book_repository.all_books()

    def book(self, id: int) -> Optional[BookModel]:
        if not is_non_negative_strict_integer(id):
            raise InvalidBookIdValueError("Book ID needs to be a non negative integer")

        return self.book_repository.book(id=id)

    def new_book(self, title: str, description: Optional[str], author: str) -> BookModel:
        if not isinstance(title, str):
            raise InvalidBookTitleValueError("Book title needs to be text")
        if description is not None and not isinstance(description, str):
            raise InvalidBookDescriptionValueError("Book description needs to be text")
        if not isinstance(author, str):
            raise InvalidBookAuthorValueError("Book author needs to be text")

        return self.book_repository.create_book(title=title, description=description, author=author)

    def update_book(self, id: int, title: Optional[str], description: Optional[str], author: Optional[str]) -> Optional[BookModel]:
        if not is_non_negative_strict_integer(id):
            raise InvalidBookIdValueError("Book ID needs to be a non negative integer")

        if title is not None and not isinstance(title, str):
            raise InvalidBookTitleValueError("Book title needs to be text")
        if description is not None and not isinstance(description, str):
            raise InvalidBookDescriptionValueError("Book description needs to be text")
        if author is not None and not isinstance(author, str):
            raise InvalidBookAuthorValueError("Book author needs to be text")

        return self.book_repository.update_book(id=id, title=title, description=description, author=author)


    def remove_book(self, id: int) -> None:
        if not is_non_negative_strict_integer(id):
            raise InvalidBookIdValueError("Book ID needs to be a non negative integer")

        self.book_repository.delete_book(id=id)
