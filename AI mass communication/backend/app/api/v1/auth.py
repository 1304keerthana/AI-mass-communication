from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth import authenticate_user, create_access_token, get_password_hash
from app.repositories.users import create_user
from app.schemas import Token, UserCreate

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate):
    hashed_password = get_password_hash(user_create.password)
    user = await create_user(
        name=user_create.name,
        email=user_create.email,
        password=hashed_password,
        role_name=user_create.role,
    )
    access_token = create_access_token(data={"sub": user.email, "role": user.role_name})
    return Token(access_token=access_token)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email, "role": user.role_name})
    return Token(access_token=access_token)
