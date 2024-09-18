from fastapi import APIRouter

from apps.books.routes import router as books_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(books_router)
