from fastapi import FastAPI
from .api.routers import todo, habit, water_goal, water_bottle, nutrition_info_ai_request, publisher
from app.db.database import Base, engine
from app.api.routers.nutri import nutriRouter

app = FastAPI()

nutriRouter.include_router(todo.router, prefix="/todo", tags=["ToDo"])
nutriRouter.include_router(habit.habit_router, prefix="/habits", tags=["Habits"])
nutriRouter.include_router(water_goal.router, prefix="/water_goal", tags=["Water Goals"])
nutriRouter.include_router(water_bottle.router, prefix="/water_bottle", tags=["Water Bottles"])
nutriRouter.include_router(nutrition_info_ai_request.router, tags=["Nutrition Info AI"])
nutriRouter.include_router(publisher.router, tags=["Delete profile's data"])

app.include_router(nutriRouter)


Base.metadata.create_all(bind=engine)