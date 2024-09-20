from fastapi import APIRouter

from apps.books.dtos import CreateBookDto

router = APIRouter(
    prefix="/books",
)


@router.get("/")
async def get_books():
    return [
        {
            "id": 1,
            "title": "Hello World!",
            "description": "Short description",
            "author": "Petar Cevriz",
        },
        {
            "id": 2,
            "title": "Hello World!",
            "description": "Short description",
            "author": "Petar Cevriz",
        },
    ]


@router.get("/{book_id}")
async def get_book(book_id: int):
    return {
        "id": book_id,
        "title": "Hello World!",
        "description": "Short description",
        "author": "Petar Cevriz",
    }


@router.post("/")
async def create_book(book: CreateBookDto):
    return book
