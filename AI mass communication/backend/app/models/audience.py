from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.base import Base


class Audience(Base):
    __tablename__ = "audience"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    occupation = Column(String(150), nullable=True)
    organization = Column(String(150), nullable=True)
    department = Column(String(150), nullable=True)
    preferred_language = Column(String(50), nullable=True)
    engagement_score = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
