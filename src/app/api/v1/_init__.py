from app.api.v1.agent import router as router_agent_v1
from fastapi import APIRouter

router = APIRouter()

router.include_router(router_agent_v1, prefix="/agent")