from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal
from app.models import Audience
from app.schemas import AudienceCreate, AudienceFilter


async def list_audience(filter_data: AudienceFilter | None = None) -> list[Audience]:
    async with AsyncSessionLocal() as session:
        query = select(Audience)
        if filter_data:
            if filter_data.preferred_language:
                query = query.where(Audience.preferred_language == filter_data.preferred_language)
            if filter_data.state:
                query = query.where(Audience.state == filter_data.state)
            if filter_data.country:
                query = query.where(Audience.country == filter_data.country)
            if filter_data.occupation:
                query = query.where(Audience.occupation == filter_data.occupation)
            if filter_data.organization:
                query = query.where(Audience.organization == filter_data.organization)
            if filter_data.department:
                query = query.where(Audience.department == filter_data.department)
            if filter_data.min_engagement_score is not None:
                query = query.where(Audience.engagement_score >= filter_data.min_engagement_score)
            if filter_data.max_engagement_score is not None:
                query = query.where(Audience.engagement_score <= filter_data.max_engagement_score)
        result = await session.execute(query)
        return result.scalars().all()


async def create_audience_member(audience_create: AudienceCreate) -> Audience:
    audience = Audience(**audience_create.model_dump())
    async with AsyncSessionLocal() as session:
        session.add(audience)
        await session.commit()
        await session.refresh(audience)
    return audience
