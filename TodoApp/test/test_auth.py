from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, ALGORITHM, SECRET_KEY, get_current_user
from fastapi import status, HTTPException
from jose import JWTError, jwt
import datetime
from datetime import timezone, timedelta
import pytest

app.dependency_overrides[get_db]=override_get_db


def test_autehenticate_user(test_user):
    db=TestingSessionLocal()

    authenticated_user=authenticate_user(test_user.username, 'password', db)
    assert authenticated_user is not None

    non_user=authenticate_user('wrong_user','password', db)
    assert non_user is False

    wrong_pwd=authenticate_user('ashish','wrong_password', db)
    assert wrong_pwd is False

def test_create_access_token(test_user):
    token=create_access_token(test_user.username,test_user.id, test_user.role, timedelta(minutes=20))
    decoded_token=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub']==test_user.username
    assert decoded_token['id']==test_user.id
    assert decoded_token['role']==test_user.role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode={'sub':'ashish', 'id':1, 'role': 'admin'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user=await get_current_user(token=token)
    assert user=={'username':'ashish','id':1,'user_role':'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode={'role':'user'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exception_info:
        await get_current_user(token=token)

    assert exception_info.value.status_code==401
    assert exception_info.value.detail=='Unauthorized User'