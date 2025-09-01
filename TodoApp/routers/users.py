from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,  HTTPException, Path, status
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..models import Todos
from ..database import SessionLocal, engine
from .auth import get_current_user
from ..models import Users

router=APIRouter(
    prefix='/users',
    tags=['users']
)


bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

class VerifyPassword(BaseModel):
    user_id: int
    old_password: str
    new_password: str

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    print(user)
    print('***************')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/update_password', status_code=status.HTTP_204_NO_CONTENT)
def update_password(user: user_dependency, db: db_dependency,verify_password: VerifyPassword):
    user=db.query(Users).filter(Users.id==verify_password.user_id).first()

    if user is None or not bcrypt_context.verify(verify_password.old_password,user.hashed_password,):
        return HTTP_401_UNAUTHORIZED
    user.hashed_password=bcrypt_context.hash(verify_password.new_password)
    return HTTP_204_NO_CONTENT

@router.put('/update_phone',status_code=status.HTTP_204_NO_CONTENT)
def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()
    