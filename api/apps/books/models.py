from pydantic import BaseModel


class BookModel(BaseModel):
    id: int
    title: str
    description: str
    author: str
