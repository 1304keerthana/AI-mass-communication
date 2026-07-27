from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth import require_active_user, require_role
from app.repositories.templates import create_template, get_template
from app.schemas import TemplateCreate, TemplateRead

router = APIRouter()


@router.post("/", response_model=TemplateRead)
async def create_template_endpoint(
    template_create: TemplateCreate,
    current_user=Depends(require_role(["admin", "manager", "communicator"])),
) -> TemplateRead:
    template = await create_template(
        title=template_create.title,
        category=template_create.category,
        content=template_create.content,
        created_by=current_user.id,
    )
    return TemplateRead.model_validate(template)


@router.get("/{template_id}", response_model=TemplateRead)
async def get_template_endpoint(template_id: int, current_user=Depends(require_active_user)) -> TemplateRead:
    template = await get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return TemplateRead.model_validate(template)
