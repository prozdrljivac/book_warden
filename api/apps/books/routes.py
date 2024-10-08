import sqlite3

from fastapi import APIRouter, Response, status

from apps.books.dtos import (
    CreateBookRequestDto,
    CreateBookResponseDto,
    GetBookResponseDto,
    ListBookResponseDto,
    UpdateBookRequestDto,
    UpdateBookResponseDto,
)

router = APIRouter(
    prefix="/books",
)


@router.get("/")
def get_books():
    with sqlite3.connect("db/dev.db") as db_connection:
        db_cursor = db_connection.cursor()
        result = db_cursor.execute(
            """
            SELECT id, title, description, author FROM books;
            """
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


@router.get("/{book_id}")
def get_book(book_id: int):
    with sqlite3.connect("db/dev.db") as db_connection:
        db_cursor = db_connection.cursor()
        result = db_cursor.execute(
            "SELECT id, title, description, author FROM books WHERE id=?",
            (book_id,),
        )
        book = result.fetchone()

        if not book:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    return GetBookResponseDto(
        id=book[0],
        title=book[1],
        description=book[2],
        author=book[3],
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(create_book_request_dto: CreateBookRequestDto):
    with sqlite3.connect("db/dev.db") as db_connection:
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


# BUG - Updates fields to None even though fields were not provided in the request
# TODO - check if user can send request without update_book_dto
@router.patch("/{book_id}")
def update_book(book_id: int, update_book_dto: UpdateBookRequestDto):
    with sqlite3.connect("db/dev.db") as db_connection:
        db_cursor = db_connection.cursor()
        result = db_cursor.execute(
            "SELECT id, title, description, author FROM books WHERE id=?",
            (book_id,),
        )
        book = result.fetchone()

        if not book:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        update_book_dct = update_book_dto.model_dump()
        update_fields = [f"{k} = ?" for k in update_book_dct.keys() if ]
        params = [v for v in update_book_dct.values()]

        if update_fields:
            query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
            # TODO need a better way to pull this id
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
    # TODO check if this is a correct response
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    with sqlite3.connect("db/dev.db") as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            """
            DELETE FROM books WHERE id = ?
            """,
            (book_id,),
        )
