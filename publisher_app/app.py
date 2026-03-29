from flask import Flask, render_template, request, redirect, url_for, flash
import pika
import os
import time
import logging

app = Flask(__name__)
app.secret_key = "qualitest_elbit_secret"  # Needed for UI flash messages

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
# Updated defaults to your specific credentials
MQ_USER = os.getenv('MQ_USER', 'eran')
MQ_PASS = os.getenv('MQ_PASS', 'likes-elbit-and-qualitest')


def get_mq_connection():
    """Establishes and returns a connection to RabbitMQ with retry logic."""
    credentials = pika.PlainCredentials(MQ_USER, MQ_PASS)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

    # Quick retry loop in case broker is restarting
    for _ in range(5):
        try:
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)
    raise Exception("Could not connect to RabbitMQ broker.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publish_default', methods=['POST'])
def publish_default():
    """Sends the original 10 assignment messages."""
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
    """Sends a user-defined custom message."""
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
    # Run on port 5001 so it doesn't conflict with other apps
    app.run(host='0.0.0.0', port=5001)