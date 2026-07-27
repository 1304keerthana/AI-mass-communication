from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class TemplateCategory(str, Enum):
    awareness = "awareness"
    emergency = "emergency"
    educational = "educational"
    announcement = "announcement"


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(SqlEnum(TemplateCategory, name="template_category"), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    creator = relationship("User", back_populates="templates")
