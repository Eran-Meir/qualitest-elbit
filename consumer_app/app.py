from flask import Flask, render_template, jsonify
import pika
import os
import threading
import time
import datetime

app = Flask(__name__)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
MQ_USER = os.getenv('MQ_USER', 'eran')
MQ_PASS = os.getenv('MQ_PASS', 'likes-elbit-and-qualitest')

# Global list to store messages in memory
messages_store = []


def rabbitmq_listener():
    """Background thread function to continuously consume messages."""
    print("[*] Starting RabbitMQ listener thread...")
    while True:
        try:
            credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
            parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Ensure the queue exists
            channel.queue_declare(queue='ABC')

            def callback(ch, method, properties, body):
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                msg_text = body.decode()
                log_entry = f"[{timestamp}] Received: {msg_text}"
                print(log_entry, flush=True)

                messages_store.append(log_entry)
                # Keep only the latest 100 messages so we don't run out of RAM
                if len(messages_store) > 100:
                    messages_store.pop(0)

            channel.basic_consume(queue='ABC', on_message_callback=callback, auto_ack=True)
            print("[*] Connected and waiting for messages...", flush=True)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ not ready or connection lost. Retrying in 5 seconds...", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"[!] Unexpected error in consumer thread: {e}", flush=True)
            time.sleep(5)


# Start the RabbitMQ listener as a background daemon thread
listener_thread = threading.Thread(target=rabbitmq_listener, daemon=True)
listener_thread.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/messages')
def get_messages():
    """API endpoint for the frontend to poll new messages."""
    return jsonify(messages_store)


if __name__ == '__main__':
    # Run on port 5002
    app.run(host='0.0.0.0', port=5002)