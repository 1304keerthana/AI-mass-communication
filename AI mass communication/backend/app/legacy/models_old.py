from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlmodel import Field, JSON, SQLModel


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    communicator = "communicator"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    role: UserRole = Field(default=UserRole.communicator, sa_column=Column("role", Enum(UserRole), nullable=False))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AudienceMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)
    preferred_language: str = Field(default="en", index=True)
    state: Optional[str] = Field(default=None, index=True)
    city: Optional[str] = Field(default=None, index=True)
    demographic_group: Optional[str] = Field(default=None)
    occupation: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)
    hierarchy_level: Optional[str] = Field(default=None)
    tags: Optional[str] = Field(default=None)
    engagement_score: float = Field(default=0.0)
    last_engaged: Optional[datetime] = Field(default=None)


class TemplateCategory(str, Enum):
    awareness = "awareness"
    emergency = "emergency"
    policy = "policy"
    announcement = "announcement"
    education = "education"


class Template(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: TemplateCategory = Field(default=TemplateCategory.awareness)
    language: str = Field(default="en")
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")


class CampaignType(str, Enum):
    awareness = "awareness"
    emergency = "emergency"
    education = "education"
    announcement = "announcement"


class Channel(str, Enum):
    email = "email"
    sms = "sms"
    whatsapp = "whatsapp"
    mobile = "mobile"
    web = "web"
    social = "social"


class CampaignStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    sent = "sent"
    completed = "completed"


class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    campaign_type: CampaignType = Field(default=CampaignType.awareness)
    channel: Channel = Field(default=Channel.email)
    status: CampaignStatus = Field(default=CampaignStatus.draft)
    template_id: Optional[int] = Field(default=None, foreign_key="template.id")
    audience_filter: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    content: Optional[str] = Field(default=None)
    translated_content: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_at: Optional[datetime] = Field(default=None)
