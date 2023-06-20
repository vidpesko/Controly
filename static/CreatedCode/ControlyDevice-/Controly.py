# Class for receiving from and sending to Controly web server
from queue import Queue

import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    print(msg, '... received on topic: ', message.topic)
    # self.message_queue.put(msg)


class Controly:
    def __init__(self, device_name, broker_url='mqtt.eclipseprojects.io'):
        self.message_queue = Queue()

        self.DEVICE_NAME = device_name
        self.broker_url = broker_url

        self.CLIENT_NAME = 'Controly_Device_' + self.DEVICE_NAME
        # On this topic will be sent changes from Controly
        self.RECEIVE_TOPIC = 'Controly/vid/' + self.DEVICE_NAME
        # Use this topic for sending back to Controly
        self.SEND_TOPIC = 'Controly/vid/device_updates'

        self.client = mqtt.Client(self.CLIENT_NAME)
        self.client.connect(self.broker_url)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        msg = message.payload.decode('utf-8')
        print(msg)
        self.message_queue.put(msg)

    def send(self, message, topic=None):
        topic = self.SEND_TOPIC if topic is None else topic
        print('sending ', message, 'on topic ', topic)

        self.client.publish(topic, message)

    def start(self, subscribe=False):
        self.client.loop_start()
        self.client.subscribe(self.RECEIVE_TOPIC)

    def close(self):
        self.client.loop_stop()