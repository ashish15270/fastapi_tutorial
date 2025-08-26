from datetime import timedelta, timezone
import datetime
from typing import Annotated
from sqlalchemy.engine import create
from sqlalchemy.orm import Session
from sqlalchemy.sql import roles
from sqlalchemy.util import deprecated
from database import SessionLocal
from models import Users
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY='OPENSSL RAND -HEX 32'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    is_active:bool

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency=Annotated[OAuth2PasswordRequestForm, Depends()]
auth_bearer_dependency=Annotated[str, Depends(oauth_bearer)]

def authenticate_user(username: str, pwd: str, db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user or not bcrypt_context.verify(pwd, user.hashed_password):
        return False
    return user

def create_access_token(user: str, user_id: int, role: str,expires_delta: timedelta):
    encode={'sub':user, 'id':user_id, 'role': role}
    expires=datetime.datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

class Token(BaseModel):
    access_token: str
    token_type: str

def get_current_user(token: auth_bearer_dependency):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get('sub')
        userid: int = payload.get('id')
        role: str=payload.get('role')
        if username is None or userid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized User')
        return {'username': username, 'id': userid, 'user_role': role}
    except JWTError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized User')

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency,create_user_request: CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=create_user_request.is_active
    )
    db.add(create_user_model)
    db.commit()

@router.post('/token/', response_model=Token)
def login_for_access_token(form_data: auth_dependency,db: db_dependency):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized User')
    token=create_access_token(user.username, user.id, user.role,timedelta(minutes=20))
    return {'access_token':token, 'token_type': 'bearer'}
