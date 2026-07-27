from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import CampaignStatus, CampaignType, TemplateCategory


class RoleName(str, Enum):
    admin = "admin"
    manager = "manager"
    communicator = "communicator"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleName] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleName = RoleName.communicator

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_name: RoleName
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AudienceCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    preferred_language: Optional[str] = "en"
    engagement_score: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class AudienceFilter(BaseModel):
    preferred_language: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    min_engagement_score: Optional[float] = None
    max_engagement_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class AudienceRead(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    occupation: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    preferred_language: Optional[str] = None
    engagement_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TemplateCreate(BaseModel):
    title: str
    category: TemplateCategory = TemplateCategory.awareness
    content: str

    model_config = ConfigDict(from_attributes=True)


class TemplateRead(BaseModel):
    id: int
    title: str
    category: TemplateCategory
    content: str
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignCreate(BaseModel):
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType = CampaignType.awareness
    schedule_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CampaignRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType
    status: CampaignStatus
    schedule_date: Optional[datetime] = None
    content: Optional[str] = None
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignAction(BaseModel):
    language: Optional[str] = "en"
    prompt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
