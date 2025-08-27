from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,  HTTPException, Path, status
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from ..models import Todos
from ..database import SessionLocal, engine
from .auth import get_current_user

router = APIRouter()

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

@router.get('/', status_code=status.HTTP_200_OK)
def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(401, detail='USer Not Authenticated')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(user: user_dependency,db: db_dependency, todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(401, detail='USer Not Authenticated')
    result=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if result is not None:
        return result
    raise HTTPException(status_code=404, detail='todo not found')

@router.post('/create_todo/', status_code=status.HTTP_201_CREATED)
def create_a_todo(user: user_dependency, db: db_dependency, todo:TodoRequest):
    if user is None:
        raise HTTPException(401, detail='USer Not Authenticated')
    todo_model=Todos(**todo.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put('/update_a_todo/{todo_id}/',status_code=status.HTTP_204_NO_CONTENT)
def update_a_todo(user: user_dependency,db: db_dependency, todo_id: int,new_todo: TodoRequest):
    if user is None:
        raise HTTPException(401, detail='USer Not Authenticated')
    todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()

    todo_model.title = new_todo.title
    todo_model.description = new_todo.description
    todo_model.priority = new_todo.priority
    todo_model.complete = new_todo.complete

    db.add(todo_model)
    db.commit()

@router.delete('/todos/delete/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency,db: db_dependency,todo_id:int = Path(gt=0) ):
  #  todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if user is None:
        raise HTTPException(401, detail='USer Not Authenticated')
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()