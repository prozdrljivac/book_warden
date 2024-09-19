from pydantic import BaseModel


class CreateBookDto(BaseModel):
    title: str
    description: str | None = None
    author: str
