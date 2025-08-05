from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

import pika
import threading
from app.api.routers.nutri import nutriRouter
from app.db.backup import run_dump
from app.db.database import Base, engine
from app.tasks.consumer import start_delete_user_objects

from .api.routers import (
    habit,
    nutrition_info_ai_request,
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

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitMQ-profile-events"))
        print("✅ Conectado ao RabbitMQ!")
        connection.close()
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")

    consumer_thread = threading.Thread(target=start_delete_user_objects, daemon=True)
    consumer_thread.start

    yield

    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)    

nutriRouter.include_router(todo.router, prefix="/todo", tags=["ToDo"])
nutriRouter.include_router(habit.habit_router, prefix="/habit", tags=["Habits"])
nutriRouter.include_router(
    water_goal.router, prefix="/water_goal", tags=["Water Goals"]
)
nutriRouter.include_router(
    water_bottle.router, prefix="/water_bottle", tags=["Water Bottles"]
)
nutriRouter.include_router(nutrition_info_ai_request.router, tags=["Nutrition Info AI"])

app.include_router(nutriRouter)
