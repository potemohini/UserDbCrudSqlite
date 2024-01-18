
from fastapi import APIRouter
from src.routes.users import router as user_rotuer
from src.routes.address import router as addr_router
router = APIRouter()

# db environment
router.include_router(user_rotuer)
router.include_router(addr_router)