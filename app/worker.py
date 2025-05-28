from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL
)