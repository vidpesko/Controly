# Class for receiving from and sending to Controly web server
from queue import Queue
import device_specific as spec

import paho.mqtt.client as mqtt

import json


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
        j = json.loads(msg)
        msg_type = j['change_type']
        payload = j['payload']
        print(j)
        self.message_queue.put((payload, msg_type))

    def send(self, message, topic=None):
        topic = self.SEND_TOPIC if topic is None else topic
        print('Sending', message, 'on topic', topic)

        self.client.publish(topic, message)

    def start(self, subscribe=False):
        self.client.loop_start()
        self.client.subscribe(self.RECEIVE_TOPIC)

    def close(self):
        self.client.loop_stop()


def handle_device_changes(changes: json, dev):
    values = {}
    fr = open('device_specific.py', 'r')

    lines = fr.readlines()
    for line in lines:
        s = line.split('=')
        values[s[0]] = s[1]

    changes = json.loads(changes.replace("'", '"'))
    for change in changes:
        field = change['field']
        new_val = change['value']

        values[field] = "'" + new_val + "'\n"

    write_l = []
    for key, val in values.items():
        write_l.append(f'{key}={val}')
    
    fw = open('device_specific.py', 'w')
    fw.writelines(write_l)
    fr.close()
    fw.close()

    dev.close()
    try:
        dev.connect(p=values['DEVICE_SERIAL_PORT'].replace("'", '').replace('\n', ''))
    except:
        print('Couldn\'t connect')