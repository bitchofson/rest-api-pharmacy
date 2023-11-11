from fastapi import APIRouter

from .pharmacy.routes import router as release_form_router

router = APIRouter()
router.include_router(router=release_form_router, prefix='/release_forms')