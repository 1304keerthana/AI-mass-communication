from fastapi import APIRouter

from app.api.v1 import auth, audience, templates, campaigns

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(audience.router, prefix="/audience", tags=["audience"])
router.include_router(templates.router, prefix="/templates", tags=["templates"])
router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])


@router.get("/status")
async def status() -> dict:
    return {"message": "API v1 is working"}
