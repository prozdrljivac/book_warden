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
    return create_book_dto


@router.patch("/{book_id}")
async def update_book(book_id: int, update_book_dto: UpdateBookDto):
    print(book_id)
    return update_book_dto


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    return book_id
