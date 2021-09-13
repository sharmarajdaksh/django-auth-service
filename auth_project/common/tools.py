import json

import pika
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from config.rabbitmq_config import RABBITMQ_HOST, RABBITMQ_EMAIL_QUEUE, RABBITMQ_EMAIL_ROUTING_KEY, RABBITMQ_PASSWORD, RABBITMQ_USER


def get_error_response(status_code: int, messages: list) -> Response:
    return Response(
        status=status_code,
        data={
            "error": messages
        }
    )


def get_success_response(status_code: int, data: dict) -> Response:
    return Response(
        status=status_code,
        data=data
    )


def is_registered_email(email: str) -> bool:
    return len(get_user_model().objects.get(email=email)) == 1


def queue_email(email, subject, content):
    message_body = json.dumps({
        "email": email,
        "subject": subject,
        "content": content,
    }).encode()

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_EMAIL_QUEUE)
    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_EMAIL_ROUTING_KEY,
        body=message_body
    )
    
    channel.close()