from fastapi import status
from .utils import *
from ..routers.admin import get_db, get_current_user
from ..models import Todos

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response=client.get('/admin/todo/')
    assert response.status_code==status.HTTP_200_OK

def test_admin_delete_todo(test_todo):
    response=client.delete('/admin/delete/1')
    assert response.status_code==status.HTTP_204_NO_CONTENT

    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None

def test_invalid_todo_delete(test_todo):
    response=client.delete('/admin/delete/899')
    assert response.status_code==status.HTTP_404_NOT_FOUND
