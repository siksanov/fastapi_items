import jwt
import secrets
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, datetime, timezone
from typing import Any, Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from models.user import User
from sqlmodel import SQLModel
from pydantic import ValidationError
from core.db import SessionGet
from core.conf import settings


class TokenPayload(SQLModel):
    sub: str | None = None


reusable_oauth2 = OAuth2PasswordBearer(
    f'{settings.API_V1_STR}/users/signin'
)

TokenGet = Annotated[str, Depends(reusable_oauth2)]


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, settings.ALGORITHM)
    return encoded_jwt


def auth_user(session: SessionGet, token: TokenGet):
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'Не удалось проверить учетные данные'
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Пользователь не найден'
        )
    if not user.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Пользователь неактивен'
        )
    return user


AuthUser = Annotated[User, Depends(auth_user)]
