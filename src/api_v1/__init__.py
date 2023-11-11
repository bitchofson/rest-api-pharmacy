from fastapi import APIRouter

from .release_forms.routes import router as release_form_router
from .manufacturers.routes import router as manufacturer_router

router = APIRouter()
router.include_router(router=release_form_router, prefix='/release_forms')
router.include_router(router=manufacturer_router, prefix='/manufacturers')