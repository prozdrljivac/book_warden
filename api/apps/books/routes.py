from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
)


@router.get("/{book_id}")
async def get_book(book_id: int):
    return {
        "id": book_id,
        "title": "Hello World!",
        "description": "Short description",
        "author": "Petar Cevriz",
    }
