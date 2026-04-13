from fastapi import APIRouter

from app.routes.iam_routes.auth_route import router as auth_router
from app.routes.iam_routes.role_routes import router as role_router
from app.routes.iam_routes.user_routes import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(role_router)
