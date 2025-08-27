from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,  HTTPException, Path, status
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..models import Todos
from ..database import SessionLocal, engine
from .auth import get_current_user
from ..models import Users

router=APIRouter(
    prefix='/admin',
    tags=['admin']
)
class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description:str=Field(min_length=3)
    priority:int=Field(gt=0,lt=6)
    complete:bool

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

@router.get('/todo/', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Unauthenticated_user')
    return db.query(Todos).all()

@router.delete('/delete/', status_code=HTTP_204_NO_CONTENT)
def delete_todos(user: user_dependency, db: db_dependency,todo_id):
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()

@router.get('/users/', status_code=status.HTTP_200_OK)
def get_all_users(user: user_dependency, db: db_dependency, user_id):
    user = db.query(Users).filter(Users.id==user_id).first()
    if user.role!='admin':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized User')
    user_info=db.query(Users).filter(Users.id==user_id).first()
    return user_info
