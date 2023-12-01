from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer
from flask_cors import CORS

from config import *
import threading
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


def consume_topic(topic, event_name):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[server_addr + ':9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    for message in consumer:
        data = message.value
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON: {data}")
                continue

        socketio.emit(event_name, data)


@socketio.on('connect')
def on_connect():
    print('Client connected')
    threading.Thread(target=consume_topic, args=(
        'drivers_topic', 'update_driver')).start()
    threading.Thread(target=consume_topic, args=(
        'requests_topic', 'update_request')).start()


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port="5050")
