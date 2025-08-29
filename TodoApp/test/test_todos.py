import os
import pytest
from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_404_NOT_FOUND
from ..database import Base
from ..main import app
from ..models import Todos
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient

sql_alchemy_url=os.getenv('SQLALCHEMY_DATABASE_URL')

engine=create_engine(sql_alchemy_url,
connect_args={'check_same_thread':False},
poolclass=StaticPool)

TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'ashish', 'id':1, 'user_role': 'admin'}

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)

@pytest.fixture
def test_todo():
    try:
        todo=Todos(
            title='Learn FastAPI',
            description='its fun',
            priority=1,
            complete=False,
            owner_id=1
        )
        
        db = TestingSessionLocal()
        db.add(todo)
        db.commit()
        yield todo
    finally:
        with engine.connect() as connection:
            connection.execute(text("DELETE FROM todos;"))
            connection.commit()

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
    assert response.json()==[{'title':'Learn FastAPI',
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

def test_create_new_todo():
    request_data={
        'title':'Learn FastAPI',
        'description':'its fun',
        'complete':False,
        'priority':1,
        'owner_id':1,
        'id':1
        }
    response=client.get('/create_todo/',request_data)
    assert response.status_code==status.HTTP_201_CREATED