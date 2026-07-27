from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.models import Template
from app.schemas import TemplateCategory


async def create_template(title: str, category: TemplateCategory, content: str, created_by: int) -> Template:
    template = Template(title=title, category=category, content=content, created_by=created_by)
    async with AsyncSessionLocal() as session:
        session.add(template)
        await session.commit()
        await session.refresh(template)
    return template


async def get_template(template_id: int) -> Template | None:
    async with AsyncSessionLocal() as session:
        return await session.get(Template, template_id)
