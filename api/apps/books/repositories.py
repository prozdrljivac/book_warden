import sqlite3
from typing import List, Optional

from apps.books.dtos import (
    CreateBookRequestDto,
    CreateBookResponseDto,
    GetBookResponseDto,
    ListBookResponseDto,
    UpdateBookRequestDto,
    UpdateBookResponseDto,
)


# TODO
# 1. Repository should not get request dto as input
# 2. Repository should return a model type, not a response dto type
class BookRepository:
    def __init__(self, db_path="db/dev.db"):
        self.db_path = db_path

    def get_books(self) -> List[ListBookResponseDto]:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            result = db_cursor.execute(
                "SELECT id, title, description, author FROM books;"
            )
            books = result.fetchall()

        return [
            ListBookResponseDto(
                id=book[0],
                title=book[1],
                description=book[2],
                author=book[3],
            )
            for book in books
        ]

    def get_book(self, book_id: int) -> Optional[GetBookResponseDto]:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            result = db_cursor.execute(
                "SELECT id, title, description, author FROM books WHERE id=?",
                (book_id,),
            )
            book = result.fetchone()
            if not book:
                return None

        return GetBookResponseDto(
            id=book[0],
            title=book[1],
            description=book[2],
            author=book[3],
        )

    def create_book(
        self,
        create_book_request_dto: CreateBookRequestDto,
    ) -> CreateBookResponseDto:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                """
                INSERT INTO books (title, description, author) VALUES (?, ?, ?)
                """,
                (
                    create_book_request_dto.title,
                    create_book_request_dto.description,
                    create_book_request_dto.author,
                ),
            )
            book_id = db_cursor.lastrowid
            db_cursor.execute(
                "SELECT id, title, description, author FROM books WHERE id = ?",
                (book_id,),
            )
            book = db_cursor.fetchone()
            db_connection.commit()

        return CreateBookResponseDto(
            id=book[0],
            title=book[1],
            description=book[2],
            author=book[3],
        )

    def update_book(
        self, book_id: int, update_book_dto: UpdateBookRequestDto
    ) -> Optional[UpdateBookResponseDto]:
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            result = db_cursor.execute(
                "SELECT id, title, description, author FROM books WHERE id=?",
                (book_id,),
            )
            book = result.fetchone()
            if not book:
                return None

            update_book_dct = update_book_dto.model_dump(exclude_none=True)
            update_fields = [f"{k} = ?" for k in update_book_dct.keys()]
            params = [v for v in update_book_dct.values()]

            if update_fields:
                query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
                params.append(book[0])

                db_cursor.execute(query, tuple(params))
                db_connection.commit()

                updated_book = db_cursor.execute(
                    "SELECT id, title, description, author FROM books WHERE id=?",
                    (book_id,),
                ).fetchone()

                return UpdateBookResponseDto(
                    id=updated_book[0],
                    title=updated_book[1],
                    description=updated_book[2],
                    author=updated_book[3],
                )

    def delete_book(self, book_id: int):
        with sqlite3.connect(self.db_path) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )
            db_connection.commit()
