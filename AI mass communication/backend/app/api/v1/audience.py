from typing import List

from fastapi import APIRouter, Depends

from app.auth.auth import require_active_user, require_role
from app.repositories.audience import create_audience_member, list_audience
from app.schemas import AudienceCreate, AudienceFilter, AudienceRead

router = APIRouter()


@router.post("/", response_model=AudienceRead)
async def add_audience_member(
    audience_create: AudienceCreate,
    current_user=Depends(require_role(["admin", "manager"])),
) -> AudienceRead:
    audience = await create_audience_member(audience_create)
    return AudienceRead.model_validate(audience)


@router.get("/", response_model=List[AudienceRead])
async def get_audience(
    preferred_language: str | None = None,
    state: str | None = None,
    country: str | None = None,
    occupation: str | None = None,
    organization: str | None = None,
    department: str | None = None,
    min_engagement_score: float | None = None,
    max_engagement_score: float | None = None,
    current_user=Depends(require_active_user),
) -> List[AudienceRead]:
    filter_data = AudienceFilter(
        preferred_language=preferred_language,
        state=state,
        country=country,
        occupation=occupation,
        organization=organization,
        department=department,
        min_engagement_score=min_engagement_score,
        max_engagement_score=max_engagement_score,
    )
    audiences = await list_audience(filter_data)
    return [AudienceRead.model_validate(item) for item in audiences]
