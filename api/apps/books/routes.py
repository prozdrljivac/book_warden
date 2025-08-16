from typing import List

from fastapi import APIRouter, Depends, Response, status

from apps.books.dtos import (
    CreateBookRequestDto,
    CreateBookResponseDto,
    GetBookResponseDto,
    ListBookResponseDto,
    UpdateBookRequestDto,
    UpdateBookResponseDto,
)
from apps.books.repositories import SQLiteBookRepository
from apps.books.services import BookService

router = APIRouter(
    prefix="/books",
)


def new_book_service():
    return BookService(book_repository=SQLiteBookRepository())


@router.get("/", response_model=List[ListBookResponseDto])
def get_books(service: BookService = Depends(new_book_service)):
    books = service.all_books()
    return [ListBookResponseDto(**book.model_dump()) for book in books]


@router.get("/{book_id}", response_model=GetBookResponseDto)
def get_book(book_id: int, service: BookService = Depends(new_book_service)):
    book = service.book(id=book_id)
    if not book:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return GetBookResponseDto(**book.model_dump())


@router.post(
    "/",
    response_model=CreateBookResponseDto,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    create_book_request_dto: CreateBookRequestDto,
    service: BookService = Depends(new_book_service),
):
    book = service.new_book(
        title=create_book_request_dto.title,
        description=create_book_request_dto.description,
        author=create_book_request_dto.author,
    )
    return CreateBookResponseDto(**book.model_dump())


@router.patch("/{book_id}", response_model=UpdateBookResponseDto)
def update_book(
    book_id: int,
    update_book_dto: UpdateBookRequestDto,
    service: BookService = Depends(new_book_service),
):
    updated_book = service.update_book(
        id=book_id,
        title=update_book_dto.title,
        description=update_book_dto.description,
        author=update_book_dto.author,
    )
    if not updated_book:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return UpdateBookResponseDto(**updated_book.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, service: BookService = Depends(new_book_service)
):
    book = service.remove_book(id=book_id)
