import pika
import time

def main():
    # 1. Establish connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 2. Declare the queue (channel) "ABC"
    # durable=False means the queue won't survive a broker restart, which is fine for this task
    queue_name = 'ABC'
    channel.queue_declare(queue=queue_name)

    print(f"[*] Publisher connected. Sending messages to channel '{queue_name}'...")

    # 3. Send 10 messages
    for i in range(1, 11):
        message = f"Hello! This is message number {i}"
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message
        )
        print(f" [x] Sent '{message}'")
        time.sleep(0.5) # Slight delay to simulate realistic publishing

    # 4. Close connection
    connection.close()
    print("[*] All messages sent. Connection closed.")

if __name__ == '__main__':
    main()