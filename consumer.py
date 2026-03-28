import pika
import sys
import os
import time


def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')

    # Add a small delay to ensure RabbitMQ is fully ready
    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}", flush=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f"[*] Waiting for messages on '{queue_name}' at {rabbitmq_host}. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main()