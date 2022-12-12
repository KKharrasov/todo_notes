from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from .models import *
from .schemas import *
from datetime import datetime, timedelta
from jose import jwt
from core.utils import get_db
from user import errors


SECRET_KEY = "8f4e9f9ae4cb3d6e6199f3a2bd05654054d7c68e170fcd12657a25374757be3e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_bearer = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise errors.login_error()
    if not verify_password(password, user.password):
        return False
    return user.id


def encode_token(**params):
    return jwt.encode(params, SECRET_KEY, algorithm='HS256')


def generate_token(user_id: int) -> AuthToken:
    now = datetime.now()
    return AuthToken(
        access_token=encode_token(
            user_id=user_id,
            purpose=TokenPurpose.access,
            exp=now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        refresh_token=encode_token(
            user_id=user_id,
            purpose=TokenPurpose.refresh,
            exp=now + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        ),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def decode_token(token: str, purpose: TokenPurpose) -> AuthTokenPayload:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=['HS256']
        )
        if payload['purpose'] != purpose:
            raise errors.bad_token()
        return AuthTokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise errors.token_expired()


def get_user_id_from_token(
        token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> int:
    if not token:
        raise errors.bad_token()
    token_payload = decode_token(token.credentials, purpose=TokenPurpose.access)
    return token_payload.user_id


async def get_current_user(
        user_id: int = Depends(get_user_id_from_token),
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise errors.user_not_found()
    return user


def verify_refresh_token(
        params: RefreshTokenParams,
        db: Session = Depends(get_db)
) -> User:
    token_payload = decode_token(params.refresh_token, purpose=TokenPurpose.refresh)
    user = db.query(User).get(token_payload.user_id)
    if not user:
        raise errors.user_not_found()
    return user
