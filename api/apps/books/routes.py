import sqlite3

from fastapi import APIRouter, Response, status

from apps.books.dtos import (
    CreateBookRequestDto,
    CreateBookResponseDto,
    GetBookResponseDto,
    ListBookResponseDto,
    UpdateBookDto,
)

router = APIRouter(
    prefix="/books",
)


@router.get("/")
async def get_books():
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
async def get_book(book_id: int):
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
async def create_book(create_book_request_dto: CreateBookRequestDto):
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


@router.patch("/{book_id}")
async def update_book(book_id: int, update_book_dto: UpdateBookDto):
    print(book_id)
    return update_book_dto


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    with sqlite3.connect("db/dev.db") as db_connection:
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            """
            DELETE FROM books WHERE id = ?
            """,
            (book_id,),
        )
