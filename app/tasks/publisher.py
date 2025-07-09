import os
import pika
import json

RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE")

def publish_delete_user(user_id: int):
    credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_DEFAULT_HOST,
        virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE_NAME, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    channel.queue_declare(queue=RABBITMQ_QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME)

    message = json.dumps({"user_id": user_id})
    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE_NAME,
        routing_key=RABBITMQ_QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[x] Mensagem enviada para deletar user_id: {user_id}")

    connection.close()
