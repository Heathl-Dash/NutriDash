from fastapi import FastAPI
from .api.routers import todo, habit
from app.db.database import Base, engine

app = FastAPI()

app.include_router(todo.router)
app.include_router(habit.router)


Base.metadata.create_all(bind=engine)