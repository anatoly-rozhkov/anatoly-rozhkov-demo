from fastapi import APIRouter
from routers.line_provider.event_router import router as line_provider_router

main_router = APIRouter(prefix="/api")
main_router.include_router(line_provider_router, tags=["Events"])
