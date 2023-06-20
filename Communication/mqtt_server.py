from Main.models import Device

from django.utils import timezone
from django.contrib import messages

import time
import threading
import paho.mqtt.client as mqtt
import json


MQTT_BROKER_URL = 'mqtt.eclipseprojects.io'

RECEIVE_TOPIC = 'Controly/vid/device_updates'

changes_dict = {}


client = mqtt.Client('Controllllly_Server')
client.connect_async(MQTT_BROKER_URL)


def on_message(client, userdata, message):
    # ! < device_name >$@< changes >$@< message_type>
    # ? Message type is used to differentiate betweem one-time messages (like 'Uspesna posodobitev','Neuspela povezava',...) and changes (like 'Gibanje zaznano xx:yy',...)
    msg = message.payload.decode('utf-8')
    print(msg)
    msg = json.loads(msg)
    device_name = msg['device']
    payload = msg['body']
    type = msg['type']

    # if type == 'one':
    # raise_message('')
    # pass
    # ? Updating changes directly to the device model
    try:
        device = Device.objects.get(name=device_name, is_scene=False)
    except:
        print('device not', device_name)
        return
    
    if type == 'status':
        device.last_status = payload
    elif (type == 'change') or (type == 'one'):
        device.changes = payload
        device.change_time = timezone.now()
        changes_dict[device_name] = payload
    elif type == 'success':
        # TODO Raise success/failure message
        pass
    
    device.save()


def publish(topic, payload, msg_type='arduino', json_param=False):
    if json_param:
        msg = json.loads('{}')
        msg['change_type'] = msg_type
        msg['payload'] = payload
        msg = json.dumps(msg)

    print('Publishing on topic', topic, msg)
    # ? Method will return exit code of publishing to the mqtt broker
    client.publish(topic, msg)


client.on_message = on_message


def subscribe():
    while True:
        client.loop_start()
        client.subscribe(RECEIVE_TOPIC)
        time.sleep(20)
        client.loop_stop()

x = threading.Thread(target=subscribe, daemon=True)

def start_t():
    while True:
        try:
            x.start()
            x.join()
        except:
            x.start()

reconnect_thread = threading.Thread(target=start_t, daemon=True)
reconnect_thread.start()