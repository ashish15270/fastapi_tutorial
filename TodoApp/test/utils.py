import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..models import Todos, Users
from fastapi.testclient import TestClient
import pytest
from passlib.context import CryptContext

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

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

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

@pytest.fixture
def test_user():
    user=Users(
    email='test_email',
    username='ashish',
    first_name='ashish',
    last_name='thegreat',
    hashed_password=bcrypt_context.hash('password'),
    role='admin',
    phone_number='Column(String, unique=True)'
    )

    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text('Delete from Users'))
        conn.commit()
