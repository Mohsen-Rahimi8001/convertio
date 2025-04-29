import pika
import json
import os


def publish_user_deleted(user_id):
    rabbitmq_host = os.getenv("RABBITMQ_HOST")
    conn_params = pika.ConnectionParameters(rabbitmq_host)
    connection = pika.BlockingConnection(conn_params)
    
    channel = connection.channel()
    
    channel.queue_declare("user_deleted")
    
    message = json.dumps({"user_id": user_id})
    
    channel.basic_publish(exchange="", routing_key="user_deleted", body=message)
    
    connection.close()
