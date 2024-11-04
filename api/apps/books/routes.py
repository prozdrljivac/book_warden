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
from apps.books.repositories import BookRepository

router = APIRouter(
    prefix="/books",
)


def get_book_repository():
    return BookRepository()


@router.get("/", response_model=List[ListBookResponseDto])
def get_books(repository: BookRepository = Depends(get_book_repository)):
    books = repository.get_books()
    return [ListBookResponseDto(**book.model_dump()) for book in books]


@router.get("/{book_id}", response_model=GetBookResponseDto)
def get_book(book_id: int, repository: BookRepository = Depends(get_book_repository)):
    book = repository.get_book(id=book_id)
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
    repository: BookRepository = Depends(get_book_repository),
):
    created_book = repository.create_book(
        title=create_book_request_dto.title,
        description=create_book_request_dto.description,
        author=create_book_request_dto.author,
    )
    return CreateBookResponseDto(**created_book.model_dump())


@router.patch("/{book_id}", response_model=UpdateBookResponseDto)
def update_book(
    book_id: int,
    update_book_dto: UpdateBookRequestDto,
    repository: BookRepository = Depends(get_book_repository),
):
    updated_book = repository.update_book(
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
    book_id: int, repository: BookRepository = Depends(get_book_repository)
):
    book = repository.get_book(id=book_id)
    if not book:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    repository.delete_book(id=book.id)
