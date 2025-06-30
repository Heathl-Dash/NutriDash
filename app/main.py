from fastapi import FastAPI
from .api.routers import todo, habit, water_goal, water_bottle, nutrition_info_ai_request
from app.db.database import Base, engine
from app.api.routers.nutri import nutriRouter

app = FastAPI()

nutriRouter.include_router(todo.router, prefix="/todo", tags=["ToDo"])
nutriRouter.include_router(habit.habit_router, prefix="/habits", tags=["Habits"])
nutriRouter.include_router(water_goal.router, prefix="/water_goal", tags=["Water Goals"])
nutriRouter.include_router(water_bottle.router, prefix="/water_bottle", tags=["Water Bottles"])
nutriRouter.include_router(nutrition_info_ai_request.router, tags=["Nutrition Info AI"])

app.include_router(nutriRouter)


Base.metadata.create_all(bind=engine)