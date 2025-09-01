from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status
from passlib.context import CryptContext

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_user(test_user):
    response=client.get('/users/')
    print(response)
    assert response.status_code==status.HTTP_200_OK
  #  assert response.json()['hashed_password']==bcrypt_context.hash('password')   hash changes everytime

def test_change_pwd_invalid_pwd(test_user):
    response=client.put('/update_password',json={'password':'wrong_password',
                                                 "new_password": "password123"})
    
    assert response.status_code==status.HTTP_401_UNAUTHORIZED