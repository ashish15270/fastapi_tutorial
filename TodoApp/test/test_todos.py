from fastapi import status
from starlette.status import HTTP_404_NOT_FOUND
from ..database import Base
from ..main import app
from ..models import Todos
from ..routers.todos import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_read_all_authenticated(test_todo):
    response=client.get('/')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{'title':'Learn FastAPI',
        'description':'its fun',
        'complete':False,
        'priority':1,
        'owner_id':1,
        'id':1
    }]

def test_read_all_authenticated(test_todo):
    response=client.get('/')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[{
        'title':'Learn FastAPI',
        'description':'its fun',
        'complete':False,
        'priority':1,
        'owner_id':1,
        'id':1
    }]

def test_read_one_authenticated(test_todo):
    response=client.get('/todo/1')
    assert response.status_code==status.HTTP_200_OK
    assert response.json()=={'title':'Learn FastAPI',
        'description':'its fun',
        'complete':False,
        'priority':1,
        'owner_id':1,
        'id':1
    }

def test_read_one_authenticated_not_found():
    response=client.get('/todo/999')
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'todo not found'}

def test_create_new_todo(test_todo):
    request_data={
        'title':'New todo',
        'description':'its fun',
        'complete':False,
        'priority':1
        }
    response=client.post('/create_todo/',json=request_data)
    assert response.status_code==status.HTTP_201_CREATED

def test_update_todo(test_todo):
    request_data={
        'title':'Learn agentic AI',
        'description':'its important',
        'complete':False,
        'priority':5
    }
    response=client.put('/update_a_todo/1',json=request_data)
    assert response.status_code==status.HTTP_204_NO_CONTENT

    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()

    assert model.title=='Learn agentic AI'

def test_delete_tod(test_todo):
    response=client.delete('/todos/delete/1')
    assert response.status_code==status.HTTP_204_NO_CONTENT

    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None
