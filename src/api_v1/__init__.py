from fastapi import APIRouter

from .release_forms.routes import router as release_form_router
from .manufacturers.routes import router as manufacturer_router
from .drugs.routes import router as drug_router
from .availabilitys.routes import router as availability_router
from .pharmacys.routes import router as pharmacy_router

router = APIRouter()
router.include_router(router=release_form_router, prefix='/release-form')
router.include_router(router=manufacturer_router, prefix='/manufacturer')
router.include_router(router=drug_router, prefix='/drug')
router.include_router(router=availability_router, prefix='/availability')
router.include_router(router=pharmacy_router, prefix='/pharmacy')