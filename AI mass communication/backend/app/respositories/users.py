from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.session import AsyncSessionLocal
from app.models import User, Role
from app.schemas import RoleName


async def get_user_by_email(email: str) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).options(selectinload(User.role)).where(User.email == email)
        )
        return result.scalar_one_or_none()


async def create_user(name: str, email: str, password: str, role_name: RoleName) -> User:
    user = User(name=name, email=email, password=password, role_id=await _get_role_id(role_name))
    async with AsyncSessionLocal() as session:
        session.add(user)
        await session.commit()
        # refresh user and also load the `role` relationship to avoid DetachedInstanceError
        await session.refresh(user)
        try:
            await session.refresh(user, attribute_names=["role"])
        except TypeError:
            # older SQLAlchemy versions may not support attribute_names param; access role to load
            _ = user.role
    return user


async def _get_role_id(role_name: RoleName) -> int:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Role).where(Role.role_name == role_name.value))
        role = result.scalar_one_or_none()
        if role:
            return role.id
        role = Role(role_name=role_name.value)
        session.add(role)
        await session.commit()
        await session.refresh(role)
        return role.id
