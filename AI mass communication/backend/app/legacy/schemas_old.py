from datetime import datetime
from typing import Dict, List, Optional

from pydantic import EmailStr
from sqlmodel import SQLModel

from .models import AudienceMember, CampaignType, Channel, CampaignStatus, TemplateCategory, UserRole


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None


class UserCreate(SQLModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.communicator


class UserRead(SQLModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class AudienceCreate(SQLModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferred_language: str = "en"
    state: Optional[str] = None
    city: Optional[str] = None
    demographic_group: Optional[str] = None
    occupation: Optional[str] = None
    organization: Optional[str] = None
    hierarchy_level: Optional[str] = None
    tags: Optional[str] = None
    engagement_score: float = 0.0


class AudienceFilter(SQLModel):
    preferred_language: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    demographic_group: Optional[str] = None
    occupation: Optional[str] = None
    organization: Optional[str] = None
    hierarchy_level: Optional[str] = None
    min_engagement_score: Optional[float] = None
    max_engagement_score: Optional[float] = None
    tags: Optional[str] = None


class TemplateCreate(SQLModel):
    title: str
    category: TemplateCategory = TemplateCategory.awareness
    language: str = "en"
    body: str


class CampaignCreate(SQLModel):
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType = CampaignType.awareness
    channel: Channel = Channel.email
    template_id: Optional[int] = None
    audience_filter: Optional[AudienceFilter] = None
    content: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class CampaignAction(SQLModel):
    language: Optional[str] = "en"
    prompt: Optional[str] = None


class CampaignRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType
    channel: Channel
    status: CampaignStatus
    audience_filter: Optional[Dict[str, str]] = None
    content: Optional[str] = None
    translated_content: Optional[Dict[str, str]] = None
    created_by: Optional[int] = None
    created_at: datetime
    scheduled_at: Optional[datetime] = None
