import os
import pika
import json
import time
from django.core.management.base import BaseCommand
from media_management.models import Video


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")


def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data.get("user_id")
    if user_id:
        deleted_count, _ = Video.objects.filter(owner_id=user_id).delete()
        print(f"{deleted_count} videos for user ID {user_id} deleted.")


class Command(BaseCommand):
    help = "Consumes user delete messages from RabbitMQ and deletes user videos"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RabbitMQ consumer for user deletion...")
        
        conn_params = pika.ConnectionParameters(RABBITMQ_HOST)
            
        connection = pika.BlockingConnection(conn_params)
        
        channel = connection.channel()
        
        channel.queue_declare(queue="user_deleted")
        
        channel.basic_consume(queue="user_deleted", on_message_callback=callback, auto_ack=True)

        self.stdout.write("Waiting for messages...")
        
        try:
            channel.start_consuming()
        
        except KeyboardInterrupt:
            self.stdout.write("Consuming stopped.")

        except Exception as e:
            self.stderr.write(f"Consumer crashed. Error: {str(e)}")
            self.stdout.write("Retrying in 3 seconds...")
            time.sleep(3)
