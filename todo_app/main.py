
from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi import templating

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates=templating.Jinja2Templates(directory='todo_app/templates')

app.get('/')
def test(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
