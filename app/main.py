from fastapi import FastAPI
from .api.routers import todo, habit, water_goal, water_bottle, nutrition_info_ai_request
from app.db.database import Base, engine

app = FastAPI()

app.include_router(todo.router)
app.include_router(habit.router)
app.include_router(water_goal.router)
app.include_router(water_bottle.router)
app.include_router(nutrition_info_ai_request.router)


Base.metadata.create_all(bind=engine)