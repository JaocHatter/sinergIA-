from app.api.v1._init__ import router as router_v1
from fastapi import APIRouter

router = APIRouter()

router.include_router(router_v1, prefix="/v1")