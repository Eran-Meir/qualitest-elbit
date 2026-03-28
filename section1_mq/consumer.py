import pika
import sys
import os


def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    mq_user = os.getenv('MQ_USER', 'guest')
    mq_pass = os.getenv('MQ_PASS', 'guest')

    # Set up the credentials
    credentials = pika.PlainCredentials(mq_user, mq_pass)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}", flush=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f"[*] Waiting for messages on '{queue_name}' at {rabbitmq_host} as user '{mq_user}'. To exit press CTRL+C",
          flush=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Exiting...", flush=True)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main()