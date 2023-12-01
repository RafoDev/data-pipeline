import random
import time
import json
from config import *
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(bootstrap_servers=server_addr+':9092')


def send_message(message, topic):
    producer.send(topic, message.encode('utf-8'))


messages = ["Hola mundo",
            "Este es un ejemplo de conteo de palabras", "Kafka con Python"]

max_width = 1000
max_height = 500
    
class Driver:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.x = random.randint(0, max_width)
        self.y = random.randint(0, max_height)
        self.status = 'free'
        # Nueva dirección inicial aleatoria
        self.direction = random.randint(0, 4)
        self.move_count = 0  # Contador de movimientos en la misma dirección
        # Número aleatorio de movimientos antes de cambiar de dirección
        self.move_limit = random.randint(5, 10)

    def update_location(self):
        # Cambia de dirección después de alcanzar el límite de movimientos
        if self.move_count >= self.move_limit:
            self.direction = random.randint(0, 4)
            self.move_count = 0
            self.move_limit = random.randint(0, 20)

        # Actualiza la ubicación basándose en la dirección
        if self.direction == 1 and self.y < max_height:  # Arriba
            self.y += 10
        elif self.direction == 2 and self.x < max_width:  # Derecha
            self.x += 10
        elif self.direction == 3 and self.y > 0:  # Abajo
            self.y -= 10
        elif self.direction == 4 and self.x > 0:  # Izquierda
            self.x -= 10

        self.move_count += 1  # Incrementa el contador de movimientos

    def __repr__(self):
        return f"Driver {self.driver_id}: ({self.x}, {self.y}), Status: {self.status}"

    def to_json(self):
        data ={
            "driver_id" : self.driver_id,
            "x": self.x,
            "y": self.y,
            "status": self.status,
            "timestamp": int(datetime.now().timestamp())
        }
        return json.dumps(data)


class Request:
    def __init__(self, request_id, existing_locations):
        self.request_id = request_id
        while True:
            self.x = random.randint(0, max_width)
            self.y = random.randint(0, max_height)
            if (self.x, self.y) not in existing_locations:
                existing_locations.add((self.x, self.y))
                break

    def __repr__(self):
        return f"Request {self.request_id}: ({self.x}, {self.y})"

    def to_json(self):
        return json.dumps(self.__dict__)


def generate_simulation(n, m, T):
    drivers = [Driver(i) for i in range(n)]
    request_locations = set()
    requests = []
    next_request_time = 0

    while True:
        if time.time() >= next_request_time:
            requests = []
            request_locations.clear()

            num_requests = random.randint(0, m)
            for request_id in range(num_requests):
                requests.append(Request(request_id, request_locations))

            next_request_time = time.time() + T

        # Update driver locations
        for driver in drivers:
            driver.update_location()

        # Display current status
        print("Drivers:")
        for driver in drivers:
            print(driver.to_json())
            send_message(driver.to_json(), "drivers_topic")

        print("\nRequests:")
        for request in requests:
            print(request.to_json())
            send_message(request.to_json(), "requests_topic")

        time.sleep(1)


# Example with 5 drivers and new requests every 5 seconds
generate_simulation(10, 4, 5)
producer.close()
