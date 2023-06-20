import communication_codes
import device_specific
from arduino import Arduino, ArduinoResponse
from Controly import Controly

import random
import json

ard = Arduino(device_specific.DEVICE_SERIAL_PORT)
con = Controly(device_specific.DEVICE_NAME)

con.start(subscribe=True)


while True:
    try:
        ard.connect()
        break
    except:
        connection_err = ArduinoResponse(response_body='Poskus povezave z Arduinom je bil neuspešen! Ponovno poskušam.')
        con.send(connection_err.get_json_response(device_specific.DEVICE_NAME, 'one'))

i = 0

while True:
    # ? 1. Checking (and sending) if there are changes from Controly:
    if not con.message_queue.empty():
        payload = con.message_queue.get_nowait()
        sending_changes_id = random.randint(0, 100)
        response = ard.ask_and_wait(communication_codes.CODE['sending_changes'], sending_changes_id, payload=payload, debug_param=True)

        # Question and answer match!
        # if response.question_id == sending_changes_id:
        # Sending response back to Controly
        con.send(response.get_json_response(device_specific.DEVICE_NAME, 'success'))

    # ? 2. Asking for any changes (like motion detected,...)
    changes_id = random.randint(0, 100)
    changes = ard.ask_and_wait(communication_codes.CODE['ask_for_changes'], changes_id, debug_param=True)

    # ? 2. Evaluating response - either '' or not empty
    # ~ 2.a True (there are changes!)
    if changes.response_body != '':
        con.send(changes.get_json_response(device_specific.DEVICE_NAME, 'change'))
    # ~ 2.b False
    else:
        msg = json.dumps({
            'device': device_specific.DEVICE_NAME,
            'body': True,
            'type': 'status',
        })

        i += 1
        if (i % 10) == 0:
            con.send(msg)

con.close()