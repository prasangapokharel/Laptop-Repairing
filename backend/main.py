from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
from users.auth import router as auth_router
from users.index import router as users_router
from devices.index import router as devices_router
from orders.index import router as orders_router
from payments.index import router as payments_router
from assigns.index import router as assigns_router

app = FastAPI(
    title="Laptop Repair Store Management API",
    version="1.0.0",
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/v1")
app.include_router(users_router, prefix="/v1")
app.include_router(devices_router, prefix="/v1")
app.include_router(orders_router, prefix="/v1")
app.include_router(payments_router, prefix="/v1")
app.include_router(assigns_router, prefix="/v1")


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)


@app.get("/")
async def root():
    return {"message": "Laptop Repair Store Management API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

