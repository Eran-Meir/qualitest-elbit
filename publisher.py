import pika
import time
import os


def main():
    # Fetch the host from environment variables, default to localhost
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')

    # Add a small delay to ensure RabbitMQ is fully ready to accept connections
    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    print(f"[*] Publisher connected to {rabbitmq_host}. Sending messages to '{queue_name}'...")

    for i in range(1, 11):
        message = f"Hello! This is message number {i}"
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent '{message}'")
        time.sleep(0.5)

    connection.close()
    print("[*] All messages sent. Connection closed.")


if __name__ == '__main__':
    main()