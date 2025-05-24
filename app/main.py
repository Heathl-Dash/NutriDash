from fastapi import FastAPI
from .api.routers import todo, habit, water_bottle
from app.db.database import Base, engine

app = FastAPI()

app.include_router(todo.router)
app.include_router(habit.router)

app.include_router(water_bottle.router)


Base.metadata.create_all(bind=engine)