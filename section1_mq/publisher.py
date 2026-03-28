import pika
import time
import os


def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    mq_user = os.getenv('MQ_USER', 'guest')
    mq_pass = os.getenv('MQ_PASS', 'guest')

    time.sleep(2)

    # Set up the credentials
    credentials = pika.PlainCredentials(mq_user, mq_pass)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    print(f"[*] Publisher connected to {rabbitmq_host} as user '{mq_user}'. Sending messages to '{queue_name}'...",
          flush=True)

    for i in range(1, 11):
        message = f"Hello! This is message number {i}"
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent '{message}'", flush=True)
        time.sleep(0.5)

    connection.close()
    print("[*] All messages sent. Connection closed.", flush=True)


if __name__ == '__main__':
    main()