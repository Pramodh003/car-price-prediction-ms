import pika
import os
from dotenv import load_dotenv
load_dotenv(".env")

RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection_parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,port=RABBITMQ_PORT,credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='vehicle_queue')
    return connection, channel