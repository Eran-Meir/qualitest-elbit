import pika
import sys
import os
import time


def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    mq_user = os.getenv('MQ_USER', 'guest')
    mq_pass = os.getenv('MQ_PASS', 'guest')

    # Retry logic to wait for RabbitMQ to be ready
    connection = None
    print(f"[*] Attempting to connect to RabbitMQ at {rabbitmq_host}...", flush=True)

    while not connection:
        try:
            credentials = pika.PlainCredentials(mq_user, mq_pass)
            parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ not ready yet, retrying in 2 seconds...", flush=True)
            time.sleep(2)

    channel = connection.channel()
    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}", flush=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"[*] Waiting for messages on '{queue_name}'. To exit press CTRL+C", flush=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Exiting...", flush=True)
        sys.exit(0)


if __name__ == '__main__':
    main()