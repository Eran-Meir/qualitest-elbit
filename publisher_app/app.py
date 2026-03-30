from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pika
import os
import time
import logging

app = Flask(__name__)
app.secret_key = "qualitest_elbit_secret"

# Silence Werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
MQ_USER = os.getenv('MQ_USER', 'eran')
MQ_PASS = os.getenv('MQ_PASS', 'likes-elbit-and-qualitest')


def get_mq_connection():
    """Establishes and returns a connection to RabbitMQ with robust retry logic."""
    credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    for _ in range(5):
        try:
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)
    # The broker is hard-down
    raise Exception("Could not connect to RabbitMQ broker.")


def send_startup_messages():
    """NEW: Internal function to send the 10 default messages on service launch."""
    print("[*] Starting Publisher Microservice...")
    try:
        # Give the broker a slight head start to complete initialization
        time.sleep(2)
        conn = get_mq_connection()
        channel = conn.channel()
        channel.queue_declare(queue='ABC')

        # Log to service output rather than UI flash
        print(f"[*] Sending 10 default startup messages to channel 'ABC'...", flush=True)
        for i in range(1, 11):
            msg = f"Hello! This is message number {i}"
            channel.basic_publish(exchange='', routing_key='ABC', body=msg)

        conn.close()
        print("[*] Default startup messages successfully sent.", flush=True)
    except Exception as e:
        print(f"[!] Error sending startup messages: {e}", flush=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publish_default', methods=['POST'])
def publish_default():
    """UI Route: Sends the original 10 assignment messages (triggered by button)."""
    try:
        conn = get_mq_connection()
        channel = conn.channel()
        channel.queue_declare(queue='ABC')

        for i in range(1, 11):
            msg = f"Hello! This is message number {i}"
            channel.basic_publish(exchange='', routing_key='ABC', body=msg)

        conn.close()
        flash("Successfully sent the 10 default messages to channel 'ABC'!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")

    return redirect(url_for('index'))


@app.route('/publish_custom', methods=['POST'])
def publish_custom():
    """UI Route: Sends a user-defined custom message."""
    message = request.form.get('custom_message', '').strip()
    if message:
        try:
            conn = get_mq_connection()
            channel = conn.channel()
            channel.queue_declare(queue='ABC')
            channel.basic_publish(exchange='', routing_key='ABC', body=message)
            conn.close()
            flash(f"Successfully sent: '{message}'", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
    else:
        flash("Cannot send an empty message.", "warning")

    return redirect(url_for('index'))


if __name__ == '__main__':
    # NEW: Trigger the automated startup routine BEFORE launching the web server.
    # It will use the internal connection retries already defined.
    send_startup_messages()

    app.run(host='0.0.0.0', port=5001)