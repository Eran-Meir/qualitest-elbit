from flask import Flask, render_template, jsonify
import pika
import os
import threading
import time
import datetime
import logging

app = Flask(__name__)

# Silence Werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
MQ_USER = os.getenv('MQ_USER', 'eran')
MQ_PASS = os.getenv('MQ_PASS', 'likes-elbit-and-qualitest')

messages_store = []
is_connected = False  # NEW: Track actual connection state


def rabbitmq_listener():
    global is_connected
    print("[*] Starting RabbitMQ listener thread...")
    while True:
        try:
            credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
            parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.queue_declare(queue='ABC')

            def callback(ch, method, properties, body):
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                msg_text = body.decode()
                log_entry = f"[{timestamp}] Received: {msg_text}"
                print(log_entry, flush=True)

                messages_store.append(log_entry)
                if len(messages_store) > 100:
                    messages_store.pop(0)

            channel.basic_consume(queue='ABC', on_message_callback=callback, auto_ack=True)
            print("[*] Connected and waiting for messages...", flush=True)

            is_connected = True  # Set to true right before blocking
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            is_connected = False  # Connection dropped!
            print("[!] RabbitMQ not ready or connection lost. Retrying in 5 seconds...", flush=True)
            time.sleep(5)
        except Exception as e:
            is_connected = False
            print(f"[!] Unexpected error: {e}", flush=True)
            time.sleep(5)


listener_thread = threading.Thread(target=rabbitmq_listener, daemon=True)
listener_thread.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/messages')
def get_messages():
    # NEW: Return a dictionary with both status and messages
    return jsonify({
        "status": "connected" if is_connected else "disconnected",
        "messages": messages_store
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)