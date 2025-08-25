from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from apps.routes import api_v1_router
from apps.exceptions import BusinessRuleException
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

@app.exception_handler(BusinessRuleException)
async def business_rule_exception_handler(request: Request, exc: BusinessRuleException):
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc)
        }
    )
