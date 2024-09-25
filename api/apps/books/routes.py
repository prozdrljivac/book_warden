import sqlite3

from fastapi import APIRouter

from apps.books.dtos import CreateBookDto, GetBookDto, ListBookDto, UpdateBookDto

router = APIRouter(
    prefix="/books",
)


@router.get("/")
async def get_books():
    return [
        ListBookDto(
            id=1,
            title="Hello World!",
            description="Short description",
            author="Petar Cevriz",
        ),
        ListBookDto(
            id=2,
            title="Hello World!",
            description="Short description",
            author="Petar Cevriz",
        ),
    ]


@router.get("/{book_id}")
async def get_book(book_id: int):
    return GetBookDto(
        id=book_id,
        title="Hello World!",
        description="Short description",
        author="Petar Cevriz",
    )


@router.post("/")
async def create_book(create_book_dto: CreateBookDto):
    db_connection = sqlite3.connect("db/dev.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        """
        INSERT INTO books (title, description, author) VALUES (?, ?, ?)
        """,
        (
            create_book_dto.title,
            create_book_dto.description,
            create_book_dto.author,
        ),
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    create_book_dto.model_dump(exclude=["id"])
    return create_book_dto


@router.patch("/{book_id}")
async def update_book(book_id: int, update_book_dto: UpdateBookDto):
    print(book_id)
    return update_book_dto


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    return book_id
