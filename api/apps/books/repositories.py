import sqlite3

from abc import ABC, abstractmethod
from typing import List, Optional

from apps.books.models import BookModel

class BookRepository(ABC):
    @abstractmethod
    def all_books(self) -> List[BookModel]:
        raise NotImplementedError

    @abstractmethod
    def book(self, id: int) -> Optional[BookModel]:
        raise NotImplementedError

    @abstractmethod
    def create_book(self, title: str, description: Optional[str], author: str) -> BookModel:
        raise NotImplementedError

    @abstractmethod
    def update_book(
            self,
            id: int,
            title: Optional[str],
            description: Optional[str],
            author: Optional[str]) -> BookModel:
        raise NotImplementedError

    @abstractmethod
    def delete_book(self, id: int) -> None:
        raise NotImplementedError

class SQLiteBookRepository(BookRepository):
    def __init__(self, db_path="db/dev.db"):
        self.db_path = db_path

    def all_books(self) -> List[BookModel]:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            query = "SELECT id, title, description, author FROM books;"
            result = db_cursor.execute(query)
            books = result.fetchall()

        return [
            BookModel(
                id=book[0],
                title=book[1],
                description=book[2],
                author=book[3],
            )
            for book in books
        ]

    def book(
        self,
        id: int,
    ) -> Optional[BookModel]:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            query = "SELECT id, title, description, author FROM books WHERE id=?"
            result = db_cursor.execute(query, (id,))
            book = result.fetchone()
            if not book:
                return None

        return BookModel(
            id=book[0],
            title=book[1],
            description=book[2],
            author=book[3],
        )

    def create_book(
        self,
        title: str,
        description: Optional[str],
        author: str,
    ) -> BookModel:
        description = description or ""
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            insert_query = (
                "INSERT INTO books (title, description, author) VALUES (?, ?, ?)"
            )
            db_cursor.execute(
                insert_query,
                (
                    title,
                    description,
                    author,
                ),
            )
            book_id = db_cursor.lastrowid
            get_book_by_id_query = (
                "SELECT id, title, description, author FROM books WHERE id = ?"
            )
            db_cursor.execute(
                get_book_by_id_query,
                (book_id,),
            )
            book = db_cursor.fetchone()
            db_connection.commit()

        return BookModel(
            id=book[0],
            title=book[1],
            description=book[2],
            author=book[3],
        )

    def update_book(
        self,
        id: int,
        title: Optional[str],
        description: Optional[str],
        author: Optional[str],
    ) -> Optional[BookModel]:
        update_fields = {}

        if title:
            update_fields["title"] = title
        if description:
            update_fields["description"] = description
        if author:
            update_fields["author"] = author

        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            get_book_by_id_query = (
                "SELECT id, title, description, author FROM books WHERE id=?"
            )

            result = db_cursor.execute(
                get_book_by_id_query,
                (id,),
            )
            book = result.fetchone()
            if not book:
                return None

            field_names = [f"{k} = ?" for k in update_fields.keys()]
            params = [v for v in update_fields.values()]

            if not field_names:
                return None

            update_book_by_id_query = (
                f"UPDATE books SET {', '.join(field_names)} WHERE id = ?"
            )
            params.append(book[0])

            db_cursor.execute(update_book_by_id_query, tuple(params))
            db_connection.commit()

            updated_book = db_cursor.execute(
                get_book_by_id_query,
                (id,),
            ).fetchone()

            return BookModel(
                id=updated_book[0],
                title=updated_book[1],
                description=updated_book[2],
                author=updated_book[3],
            )


    def delete_book(
        self,
        id: int,
    ) -> None:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            delete_book_by_id_query = "DELETE FROM books WHERE id = ?"
            db_cursor.execute(
                delete_book_by_id_query,
                (id,),
            )
            db_connection.commit()
