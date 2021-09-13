import smtplib
import os
import pika
import json


RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_EMAIL_QUEUE = os.environ.get("RABBITMQ_EMAIL_QUEUE")
RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SMTP_SENDER_PASSWORD")

smtp_connection = smtplib.SMTP("smtp.gmail.com", 587)

rabbitmq_credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
rabbitmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=rabbitmq_credentials))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue=RABBITMQ_EMAIL_QUEUE)


def send_email(receiver_email, subject, content):
    smtp_connection.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtp_connection.sendmail(
            SENDER_EMAIL, 
            receiver_email, 
            f"Subject: {subject}\n\n{content}")
    smtp_connection.close()


def rabbitmq_email_callback(channel, method, properties, body):
    data = json.loads(body.decode())
    send_email(data["email"], data["subject"], data["content"])


rabbitmq_channel.basic_consume(
        queue=RABBITMQ_EMAIL_QUEUE,
        on_message_callback=rabbitmq_email_callback,
        auto_ack=True)

rabbitmq_channel.start_consuming()

