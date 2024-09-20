from pydantic import BaseModel


class CreateBookDto(BaseModel):
    title: str
    description: str | None = None
    author: str


class UpdateBookDto(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
