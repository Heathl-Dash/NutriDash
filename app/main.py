from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from app.api.routers.nutri import nutriRouter
from app.db.backup import run_dump
from app.db.database import Base, engine

from .api.routers import (
    habit,
    nutrition_info_ai_request,
    publisher,
    todo,
    water_bottle,
    water_goal,
)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_dump, "interval", hours=24)
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)
nutriRouter.include_router(todo.router, prefix="/todo", tags=["ToDo"])
nutriRouter.include_router(habit.habit_router, prefix="/habit", tags=["Habits"])
nutriRouter.include_router(
    water_goal.router, prefix="/water_goal", tags=["Water Goals"]
)
nutriRouter.include_router(
    water_bottle.router, prefix="/water_bottle", tags=["Water Bottles"]
)
nutriRouter.include_router(nutrition_info_ai_request.router, tags=["Nutrition Info AI"])
nutriRouter.include_router(publisher.router, tags=["Delete profile's data"])

app.include_router(nutriRouter)
