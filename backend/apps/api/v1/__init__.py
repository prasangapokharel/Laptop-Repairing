from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .devices import router as devices_router
from .orders import router as orders_router
from .payments import router as payments_router
from .assigns import router as assigns_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(devices_router)
api_router.include_router(orders_router)
api_router.include_router(payments_router)
api_router.include_router(assigns_router)

__all__ = ["api_router"]

