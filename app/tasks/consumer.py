import json
import os

import pika
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.crud.crud_water_goal import create_water_goal
from app.db.database import SessionLocal
from app.models.habits import Habit
from app.models.todo import ToDo
from app.models.waterGoal import WaterBottle, WaterGoal
from app.schemas.waterGoal import WaterGoalCreate

load_dotenv()

RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_PORT = os.getenv("RABBITMQ_DEFAULT_PORT")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE")


def __get_connection_and_channel():
    print(RABBITMQ_DEFAULT_USER)
    credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_DEFAULT_HOST,
        port=int(RABBITMQ_DEFAULT_PORT),
        virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return connection, channel


def start_delete_user_objects():
    connection, channel = __get_connection_and_channel()

    channel.exchange_declare(
        exchange=RABBITMQ_EXCHANGE_NAME,
        exchange_type=RABBITMQ_EXCHANGE_TYPE,
        durable=True,
    )
    channel.queue_declare(RABBITMQ_QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME)

    def callback(ch, method, properties, body):
        print("Mensagem recebida")
        data = json.loads(body)
        user_id = data.get("user_id")
        event = data.get("event")
        if user_id is None:
            print("user_id não informado na mensagem")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if event == "delete":
            db: Session = SessionLocal()
            try:
                db.query(Habit).filter(Habit.keycloak_id == user_id).delete(
                    synchronize_session=False
                )
                db.query(ToDo).filter(ToDo.user_id == user_id).delete(
                    synchronize_session=False
                )
                db.query(WaterGoal).filter(WaterGoal.user_id == user_id).delete(
                    synchronize_session=False
                )
                db.query(WaterBottle).filter(WaterBottle.user_id == user_id).delete(
                    synchronize_session=False
                )
                db.commit()
                print(f"Objetos deletados para user_id {user_id}")
            except Exception as e:
                db.rollback()
                print(f"Erro ao deletar objetos: {e}")
            finally:
                db.close()
        elif event == "create":
            db: Session = SessionLocal()
            try:
                weight = data.get("weight")
                water_goal_data = WaterGoalCreate(weight=weight, ml_drinked=0)
                create_water_goal(
                    db=db, keycloak_id=user_id, water_goal=water_goal_data
                )
            except Exception as e:
                db.rollback()
                print(f"Erro ao criar meta de água: {e}")
            finally:
                db.close()
        print(event)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=False
    )

    channel.start_consuming()
    connection.close()
