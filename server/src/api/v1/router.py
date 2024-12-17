from fastapi import APIRouter
from src.api.v1.routes.auth import router as auth_router
from src.api.v1.routes.tasks import router as tasks_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(tasks_router)