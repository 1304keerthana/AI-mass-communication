from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import AsyncSessionLocal
from app.models import Campaign, CampaignStatus
from app.schemas import CampaignType


async def create_campaign(title: str, description: str | None, campaign_type: CampaignType, schedule_date: datetime | None, created_by: int) -> Campaign:
    campaign = Campaign(
        title=title,
        description=description,
        campaign_type=campaign_type,
        status=CampaignStatus.draft,
        schedule_date=schedule_date,
        created_by=created_by,
    )
    async with AsyncSessionLocal() as session:
        session.add(campaign)
        await session.commit()
        await session.refresh(campaign)
    return campaign


async def list_campaigns() -> list[Campaign]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Campaign))
        return result.scalars().all()


async def get_campaign(campaign_id: int) -> Campaign | None:
    async with AsyncSessionLocal() as session:
        return await session.get(Campaign, campaign_id)


async def update_campaign_status(campaign_id: int, status: CampaignStatus) -> Campaign | None:
    async with AsyncSessionLocal() as session:
        campaign = await session.get(Campaign, campaign_id)
        if campaign:
            campaign.status = status
            session.add(campaign)
            await session.commit()
            await session.refresh(campaign)
        return campaign
