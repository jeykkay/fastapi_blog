from select import select
from typing import List

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from async_db import get_db
from jose import jwt, JWTError
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import models
import schemas


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = 'qwerty'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="users/login")


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


async def get_user(db: AsyncSession, email):
    async with db:
        result = await db.execute(select(models.User).filter(models.User.email == email))
        return result.scalars().first()


@router.post('/register/', response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = PWD_CONTEXT.hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
