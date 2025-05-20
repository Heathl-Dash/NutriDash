from fastapi import FastAPI
from .api.routers import todo

app = FastAPI()

app.include_router(todo.router)
