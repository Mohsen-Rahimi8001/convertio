import os
import pika
import threading
import json
import utils
import time



def consume_from(queue_name, callback, auto_ack=True, retries=10, delay=2):

    for attempt in range(retries):
        try:
            RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
            if not RABBITMQ_HOST:
                raise ValueError("RABBITMQ_HOST not set")
            
            conn_params = pika.ConnectionParameters(RABBITMQ_HOST)
            connection = pika.BlockingConnection(conn_params)

        except pika.exceptions.AMQPConnectionError:
            print(f"[{attempt + 1}/{retries}] RabbitMQ not ready. Retrying in {delay}s...")
            time.sleep(delay)

    if not connection:
        raise Exception("Could not connect to RabbitMQ after multiple retries.")
    
    print("[+] Connection Stablished!")
    
    channel = connection.channel()

    channel.queue_declare(queue_name)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=auto_ack)
    
    print(f"Started consuming {queue_name}.")
    
    channel.start_consuming()


# CALLBACK FUNCTIONS
def convert_video_callback(ch, method, properties, body):
    data = json.loads(body)
    
    operation_type = data.get("operation", None)
    if operation_type:
        if operation_type.lower() == "reverse":
            
            file_path = data.get("file_path", None)
            output_path = data.get("output_path", None)
            
            if file_path and output_path:
                utils.reverse_video(file_path, output_path)

    
queue_names = [
    ("video_convert", convert_video_callback),
]

for q, callback in queue_names:
    t = threading.Thread(target=consume_from, args=(q, callback))
    
    t.start()
