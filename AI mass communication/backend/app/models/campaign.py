from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class CampaignType(str, Enum):
    awareness = "awareness"
    emergency = "emergency"
    notification = "notification"
    announcement = "announcement"


class CampaignStatus(str, Enum):
    draft = "draft"
    review = "review"
    scheduled = "scheduled"
    sent = "sent"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    campaign_type = Column(SqlEnum(CampaignType, name="campaign_type"), nullable=False)
    status = Column(SqlEnum(CampaignStatus, name="campaign_status"), nullable=False, default=CampaignStatus.draft)
    schedule_date = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    creator = relationship("User", back_populates="campaigns")
