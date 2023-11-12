from fastapi import APIRouter

from .release_forms.routes import router as release_form_router
from .manufacturers.routes import router as manufacturer_router
from .drugs.routes import router as drug_router

router = APIRouter()
router.include_router(router=release_form_router, prefix='/release_forms')
router.include_router(router=manufacturer_router, prefix='/manufacturers')
router.include_router(router=drug_router, prefix='/drugs')