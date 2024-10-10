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


# TODO look into depends more
def get_book_repository():
    return BookRepository()


@router.get("/", response_model=List[ListBookResponseDto])
def get_books(repository: BookRepository = Depends(get_book_repository)):
    return repository.get_books()


@router.get("/{book_id}", response_model=GetBookResponseDto)
def get_book(book_id: int, repository: BookRepository = Depends(get_book_repository)):
    book = repository.get_book(book_id)
    if not book:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return book


@router.post(
    "/",
    response_model=CreateBookResponseDto,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    create_book_request_dto: CreateBookRequestDto,
    repository: BookRepository = Depends(get_book_repository),
):
    return repository.create_book(create_book_request_dto)


@router.patch("/{book_id}", response_model=UpdateBookResponseDto)
def update_book(
    book_id: int,
    update_book_dto: UpdateBookRequestDto,
    repository: BookRepository = Depends(get_book_repository),
):
    updated_book = repository.update_book(book_id, update_book_dto)
    if not updated_book:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int, repository: BookRepository = Depends(get_book_repository)
):
    repository.delete_book(book_id)
