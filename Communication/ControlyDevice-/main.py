from communication_codes import CODE
import device_specific
from arduino import Arduino, ArduinoResponse, SerialMonitor
from Controly import Controly, handle_device_changes

import random
import json

ard = Arduino(device_specific.DEVICE_SERIAL_PORT)
con = Controly(device_specific.DEVICE_NAME)

con.start(subscribe=True)


while True:
    try:
        ard.connect()
        suc = ArduinoResponse(response_body='Poskus povezave z Arduinom je bil uspešen! Povezava vzpostavljena')
        con.send(suc.get_json_response(device_specific.DEVICE_NAME, 'one'))
        break
    except:
        connection_err = ArduinoResponse(response_body='Poskus povezave z Arduinom je bil neuspešen! Ponovno poskušam.')
        con.send(connection_err.get_json_response(device_specific.DEVICE_NAME, 'one'))

ser_mon = SerialMonitor(ard.ser, con)
ser_mon.start()

while True:
    # ? 1. Checking (and sending) if there are changes from Controly:
    if not con.message_queue.empty():
        payload, msg_type = con.message_queue.get_nowait()
        payload = str(payload)

        # * If message type is 'device_change', than payload is changes for device_specific.py (e.g.: change to serial port...)
        if msg_type == 'device_change':
            handle_device_changes(payload, ard)
        elif msg_type == 'arduino':
            id = random.randint(0, 100)
            try:
                ard.ask(CODE['sending_changes'], id, payload=payload, debug_param=True)
            except:
                print('Couldnt ask!')

    # # ? 2. Asking for any changes (like motion detected,...)
    # changes_id = random.randint(0, 100)
    # changes = ard.ask_and_wait(communication_codes.CODE['ask_for_changes'], changes_id, debug_param=True)

    # # ? 2. Evaluating response - either '' or not empty
    # # ~ 2.a True (there are changes!)
    # if changes.response_body != '':
    #     con.send(changes.get_json_response(device_specific.DEVICE_NAME, 'change'))
    # # ~ 2.b False
    # else:
    #     msg = json.dumps({
    #         'device': device_specific.DEVICE_NAME,
    #         'body': True,
    #         'type': 'status',
    #     })

    #     i += 1
    #     if (i % 10) == 0:
    #         con.send(msg)

con.close()