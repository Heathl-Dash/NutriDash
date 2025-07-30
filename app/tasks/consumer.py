import os
import pika
import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.habits import Habit
from app.models.todo import ToDo
from app.models.waterGoal import WaterGoal, WaterBottle

RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE")

def __get_connection_and_channel():
    credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_DEFAULT_HOST,
        virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return connection, channel


def start_delete_user_objects():
    connection, channel = __get_connection_and_channel()

    channel.exchange_declare(
        exchange=RABBITMQ_EXCHANGE_NAME, 
        exchange_type=RABBITMQ_EXCHANGE_TYPE
    )
    channel.queue_declare(RABBITMQ_QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME)

    def callback(ch, method, properties, body):
        print('Mensagem recebida')
        data = json.loads(body)
        user_id = data.get("user_id")
        if user_id is None:
            print("user_id não informado na mensagem")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        db: Session = SessionLocal()
        try:
            db.query(Habit).filter(Habit.user_id == user_id).delete(synchronize_session=False)
            db.query(ToDo).filter(ToDo.user_id == user_id).delete(synchronize_session=False)
            db.query(WaterGoal).filter(WaterGoal.user_id == user_id).delete(synchronize_session=False)
            db.query(WaterBottle).filter(WaterBottle.user_id==user_id).delete(synchronize_session=False)
            db.commit()
            print(f"Objetos deletados para user_id {user_id}")
        except Exception as e:
            db.rollback()
            print(f"Erro ao deletar objetos: {e}")
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False
    )

    print("Esperando mensagens...")
    channel.start_consuming()