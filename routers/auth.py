from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.utils import get_db
from user import errors, service
from user.responses import with_errors
from user.models import User
from user.schemas import *


auth_router = APIRouter()


@auth_router.post('/api/v1/signup', response_model=UserCreate,
                  responses=with_errors(errors.bad_token, errors.user_already_exists),
                  )
def sign_up(
        params: UserCreate,
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == params.email).first()
    if user is not None:
        raise errors.user_already_exists()
    user = User(**params.dict())
    user.password = service.get_password_hash(user.password)
    user.created_timestamp = datetime.now()
    db.add(user)
    db.flush()
    return user


@auth_router.post('/api/v1/signin',
                  response_model=AuthToken,
                  responses=with_errors(errors.bad_token, errors.login_error),
                  )
def sign_in(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    user_id = service.authenticate_user(username, password, db)
    return service.generate_token(user_id)


@auth_router.put('/api/v1/changePassword',
                 response_model=UserCreate,
                 responses=with_errors(errors.bad_token, errors.user_not_found),
                 )
def change_password(
        new_pass: str,
        user: User = Depends(service.get_current_user),
        db: Session = Depends(get_db)
):
    user.password = service.get_password_hash(new_pass)
    user.updated_timestamp = datetime.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@auth_router.post("/token", response_model=AuthToken)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.generate_token(user)


@auth_router.post('/refresh',
                  response_model=AuthToken,
                  responses=with_errors(errors.bad_token),
                  )
def refresh_token(
    user: User = Depends(service.verify_refresh_token),
    db: Session = Depends(get_db)
):
    return service.generate_token(user.id)
