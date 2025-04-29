import pika
import os
import json


def publish_video_reverse_convert(video_path, output_path, operation):
    rabbitmq_host = os.getenv("RABBITMQ_HOST")
    
    conn_params = pika.ConnectionParameters(rabbitmq_host)
    
    connection = pika.BlockingConnection(conn_params)
    
    channel = connection.channel()
    
    channel.queue_declare("video_convert")

    data = json.dumps(
        {
            "file_path": video_path,
            
            "output_path": output_path,
            
            "operation": operation
        }
    )
    
    channel.basic_publish(exchange="", routing_key="video_convert", body=data)
    
    connection.close()

    