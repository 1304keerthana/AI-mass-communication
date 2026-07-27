from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from . import auth, database, models, schemas


def get_user_by_email(email: str) -> Optional[models.User]:
    with Session(database.engine) as session:
        return session.exec(select(models.User).where(models.User.email == email)).first()


def create_user(user_create: schemas.UserCreate) -> models.User:
    user = models.User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=auth.get_password_hash(user_create.password),
        role=user_create.role,
    )
    with Session(database.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def list_audience(filter_data: Optional[schemas.AudienceFilter] = None) -> List[models.AudienceMember]:
    with Session(database.engine) as session:
        query = select(models.AudienceMember)
        if filter_data:
            if filter_data.preferred_language:
                query = query.where(models.AudienceMember.preferred_language == filter_data.preferred_language)
            if filter_data.state:
                query = query.where(models.AudienceMember.state == filter_data.state)
            if filter_data.city:
                query = query.where(models.AudienceMember.city == filter_data.city)
            if filter_data.demographic_group:
                query = query.where(models.AudienceMember.demographic_group == filter_data.demographic_group)
            if filter_data.occupation:
                query = query.where(models.AudienceMember.occupation == filter_data.occupation)
            if filter_data.organization:
                query = query.where(models.AudienceMember.organization == filter_data.organization)
            if filter_data.hierarchy_level:
                query = query.where(models.AudienceMember.hierarchy_level == filter_data.hierarchy_level)
            if filter_data.min_engagement_score is not None:
                query = query.where(models.AudienceMember.engagement_score >= filter_data.min_engagement_score)
            if filter_data.max_engagement_score is not None:
                query = query.where(models.AudienceMember.engagement_score <= filter_data.max_engagement_score)
            if filter_data.tags:
                query = query.where(models.AudienceMember.tags.contains(filter_data.tags))
        return session.exec(query).all()


def create_audience_member(audience_create: schemas.AudienceCreate) -> models.AudienceMember:
    member = models.AudienceMember(**audience_create.dict())
    with Session(database.engine) as session:
        session.add(member)
        session.commit()
        session.refresh(member)
    return member


def create_template(template_create: schemas.TemplateCreate, created_by: int) -> models.Template:
    template = models.Template(**template_create.dict(), created_by=created_by)
    with Session(database.engine) as session:
        session.add(template)
        session.commit()
        session.refresh(template)
    return template


def get_template(template_id: int) -> Optional[models.Template]:
    with Session(database.engine) as session:
        return session.get(models.Template, template_id)


def create_campaign(campaign_create: schemas.CampaignCreate, created_by: int) -> models.Campaign:
    audience_filter = campaign_create.audience_filter.dict() if campaign_create.audience_filter else None
    campaign = models.Campaign(
        title=campaign_create.title,
        description=campaign_create.description,
        campaign_type=campaign_create.campaign_type,
        channel=campaign_create.channel,
        template_id=campaign_create.template_id,
        audience_filter=audience_filter,
        content=campaign_create.content,
        scheduled_at=campaign_create.scheduled_at,
        created_by=created_by,
    )
    with Session(database.engine) as session:
        session.add(campaign)
        session.commit()
        session.refresh(campaign)
    return campaign


def get_campaign(campaign_id: int) -> Optional[models.Campaign]:
    with Session(database.engine) as session:
        return session.get(models.Campaign, campaign_id)


def list_campaigns() -> List[models.Campaign]:
    with Session(database.engine) as session:
        return session.exec(select(models.Campaign)).all()


def update_campaign_status(campaign: models.Campaign, status: models.CampaignStatus) -> models.Campaign:
    with Session(database.engine) as session:
        campaign_in_db = session.get(models.Campaign, campaign.id)
        if campaign_in_db:
            campaign_in_db.status = status
            session.add(campaign_in_db)
            session.commit()
            session.refresh(campaign_in_db)
            return campaign_in_db
    return campaign


def record_engagement(member_id: int) -> None:
    with Session(database.engine) as session:
        member = session.get(models.AudienceMember, member_id)
        if member:
            member.engagement_score += 1.0
            member.last_engaged = datetime.utcnow()
            session.add(member)
            session.commit()
