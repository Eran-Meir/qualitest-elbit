import pika
import sys
import os


def main():
    # 1. Establish connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 2. Declare the queue "ABC" (Idempotent: ensures it exists before we try to consume)
    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    # 3. Define the callback function for when a message is received
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    # 4. Subscribe to the channel
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True  # Automatically acknowledge messages once received
    )

    print(f"[*] Waiting for messages on channel '{queue_name}'. To exit press CTRL+C")

    # 5. Start consuming
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