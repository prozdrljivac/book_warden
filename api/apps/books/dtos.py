from pydantic import BaseModel


# Rename these into Request and Response
class GetBookResponseDto(BaseModel):
    id: int
    title: str
    description: str
    author: str


class ListBookResponseDto(BaseModel):
    id: int
    title: str
    description: str
    author: str


class CreateBookRequestDto(BaseModel):
    title: str
    description: str | None = None
    author: str


class CreateBookResponseDto(BaseModel):
    id: int
    title: str
    description: str
    author: str


class UpdateBookRequestDto(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None


class UpdateBookResponseDto(BaseModel):
    id: int
    title: str
    description: str
    author: str
