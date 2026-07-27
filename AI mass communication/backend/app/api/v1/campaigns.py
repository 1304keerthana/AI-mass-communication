from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import require_active_user, require_role
from app.repositories.campaigns import create_campaign, get_campaign, list_campaigns, update_campaign_status
from app.repositories.templates import get_template
from app.schemas import CampaignAction, CampaignCreate, CampaignRead
from app.services.ai_service import AIService
from app.models import CampaignStatus as CampaignStatusModel

router = APIRouter()


@router.post("/", response_model=CampaignRead)
async def create_campaign_endpoint(
    campaign_create: CampaignCreate,
    current_user=Depends(require_role(["admin", "manager"])),
) -> CampaignRead:
    if campaign_create.title is None:
        raise HTTPException(status_code=400, detail="Title is required")
    campaign = await create_campaign(
        title=campaign_create.title,
        description=campaign_create.description,
        campaign_type=campaign_create.campaign_type,
        schedule_date=campaign_create.schedule_date,
        created_by=current_user.id,
    )
    return CampaignRead.model_validate(campaign)


@router.get("/", response_model=List[CampaignRead])
async def list_campaigns_endpoint(current_user=Depends(require_active_user)) -> List[CampaignRead]:
    campaigns = await list_campaigns()
    return [CampaignRead.model_validate(c) for c in campaigns]


@router.post("/{campaign_id}/generate")
async def generate_campaign_content(
    campaign_id: int,
    action: CampaignAction,
    current_user=Depends(require_role(["admin", "manager", "communicator"])),
) -> Dict[str, Any]:
    campaign = await get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    prompt = action.prompt or campaign.title
    generated = AIService.generate_content(prompt, language=action.language or "en")
    translated = AIService.translate_text(generated, action.language or "en")
    campaign.content = generated
    return {"generated": generated, "translated": translated}


@router.post("/{campaign_id}/send")
async def send_campaign(campaign_id: int, current_user=Depends(require_role(["admin", "manager"]))):
    campaign = await update_campaign_status(campaign_id, CampaignStatusModel.sent)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"status": str(campaign.status), "message": "Campaign queued for distribution"}
