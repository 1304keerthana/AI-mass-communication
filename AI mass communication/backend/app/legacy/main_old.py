from datetime import datetime
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from . import auth, crud, database, models, schemas
from .llm_service import AIService

app = FastAPI(title="Multilingual Mass Communication Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    database.init_db()


@app.post("/auth/register", response_model=schemas.UserRead)
def register(user_create: schemas.UserCreate) -> schemas.UserRead:
    try:
        user = crud.create_user(user_create)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return schemas.UserRead.from_orm(user)


@app.post("/auth/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role.value})
    return schemas.Token(access_token=access_token)


@app.post("/audience", response_model=models.AudienceMember)
def add_audience_member(
    audience_create: schemas.AudienceCreate,
    current_user: models.User = Depends(auth.require_role([models.UserRole.admin, models.UserRole.manager])),
) -> models.AudienceMember:
    return crud.create_audience_member(audience_create)


@app.get("/audience", response_model=List[models.AudienceMember])
def get_audience(
    preferred_language: str | None = None,
    state: str | None = None,
    city: str | None = None,
    demographic_group: str | None = None,
    occupation: str | None = None,
    organization: str | None = None,
    hierarchy_level: str | None = None,
    min_engagement_score: float | None = None,
    max_engagement_score: float | None = None,
    tags: str | None = None,
    current_user: models.User = Depends(auth.require_active_user),
) -> List[models.AudienceMember]:
    filter_data = schemas.AudienceFilter(
        preferred_language=preferred_language,
        state=state,
        city=city,
        demographic_group=demographic_group,
        occupation=occupation,
        organization=organization,
        hierarchy_level=hierarchy_level,
        min_engagement_score=min_engagement_score,
        max_engagement_score=max_engagement_score,
        tags=tags,
    )
    return crud.list_audience(filter_data)


@app.post("/templates", response_model=models.Template)
def create_template(
    template_create: schemas.TemplateCreate,
    current_user: models.User = Depends(auth.require_role([models.UserRole.admin, models.UserRole.manager, models.UserRole.communicator])),
) -> models.Template:
    return crud.create_template(template_create, created_by=current_user.id)


@app.get("/templates/{template_id}", response_model=models.Template)
def get_template(template_id: int, current_user: models.User = Depends(auth.require_active_user)) -> models.Template:
    template = crud.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@app.post("/campaigns", response_model=models.Campaign)
def create_campaign(
    campaign_create: schemas.CampaignCreate,
    current_user: models.User = Depends(auth.require_role([models.UserRole.admin, models.UserRole.manager])),
) -> models.Campaign:
    if campaign_create.template_id:
        template = crud.get_template(campaign_create.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
    campaign = crud.create_campaign(campaign_create, created_by=current_user.id)
    return campaign


@app.get("/campaigns", response_model=List[models.Campaign])
def list_campaigns(current_user: models.User = Depends(auth.require_active_user)) -> List[models.Campaign]:
    return crud.list_campaigns()


@app.post("/campaigns/{campaign_id}/generate")
def generate_campaign_content(
    campaign_id: int,
    action: schemas.CampaignAction,
    current_user: models.User = Depends(auth.require_role([models.UserRole.admin, models.UserRole.manager, models.UserRole.communicator])),
) -> Dict[str, Any]:
    campaign = crud.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    prompt = action.prompt or campaign.title
    generated = AIService.generate_content(prompt, language=action.language or "en")
    translated = AIService.translate_text(generated, action.language or "en")
    campaign.content = generated
    campaign.translated_content = {action.language or "en": translated}
    return {"generated": generated, "translated": translated}


@app.post("/campaigns/{campaign_id}/segment")
def segment_campaign_audience(
    campaign_id: int,
    current_user: models.User = Depends(auth.require_active_user),
) -> Dict[str, Any]:
    campaign = crud.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    members = [m.dict() for m in crud.list_audience()]
    filter_data = campaign.audience_filter or {}
    segments = AIService.build_audience_segments(members, filter_data)
    return {"audience_size": len(segments), "segments": segments}


@app.post("/campaigns/{campaign_id}/send")
def send_campaign(
    campaign_id: int,
    current_user: models.User = Depends(auth.require_role([models.UserRole.admin, models.UserRole.manager])),
) -> Dict[str, str]:
    campaign = crud.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign = crud.update_campaign_status(campaign, models.CampaignStatus.sent)
    return {"status": str(campaign.status), "message": "Campaign queued for distribution"}


@app.post("/audience/{member_id}/engage")
def record_engagement(member_id: int, current_user: models.User = Depends(auth.require_active_user)) -> Dict[str, str]:
    crud.record_engagement(member_id)
    return {"message": "Engagement recorded"}
