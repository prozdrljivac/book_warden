from pydantic import BaseModel


class GetBookDto(BaseModel):
    id: int
    title: str
    description: str
    author: str


class ListBookDto(BaseModel):
    id: int
    title: str
    description: str
    author: str


class CreateBookDto(BaseModel):
    title: str
    description: str | None = None
    author: str


class UpdateBookDto(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
