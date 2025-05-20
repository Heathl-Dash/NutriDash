from fastapi import FastAPI
from .api.routers import todo
from app.db.database import Base, engine

app = FastAPI()

app.include_router(todo.router)

Base.metadata.create_all(bind=engine)