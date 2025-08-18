from contextlib import asynccontextmanager
from fastapi import FastAPI

from apps.routes import api_v1_router
from db.setup import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#lifespan-events
    """
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router)

