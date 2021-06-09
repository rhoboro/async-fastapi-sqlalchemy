from fastapi import APIRouter

from .notebooks.views import router as notebooks_router
from .notes.views import router as notes_router

router = APIRouter()
router.include_router(notes_router)
router.include_router(notebooks_router)
