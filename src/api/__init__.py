# Third Party Library
from fastapi import APIRouter

from .product.crud import router as crud_router

router = APIRouter()
router.include_router(
	router=crud_router,
)
