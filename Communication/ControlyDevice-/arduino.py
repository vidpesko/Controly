# Vid Pesko
# ! Every Controly Device will need this code
# ? Here is everything for a device to:
# * connect to arduino via serial communication
# * send data to arduino
# * receive data back from arduino

from communication_codes import CODE
import device_specific as spec

from serial import Serial
import time
import json
import threading


class Arduino:
    def __init__(self, ser_port) -> None:
        self.ser = Serial(baudrate=9600)
        self.ser.port = ser_port
        self.state = 0

    def connect(self, p=None):
        if p is not None:
            self.ser.port = p
        self.ser.open()
        time.sleep(2)
        print('Connected to', self.ser.name)

    def ask(self, code: int, question_id: int, payload: str = None, bool_param: bool = False, debug_param: bool = True):
        # question_id is used as fail-safe -> to check if question and answer match
        start_t = time.time() * 1000

        # Ask arduino
        if payload is not None:
            payload = payload.replace('True', 'true')
            payload = payload.replace('False', 'false')
        else:
            payload = 'empty_payload'

        message = str(code) + '*' + str(question_id) + '*' + payload + '\n'
        message = message.replace("'", '"')
        message = message.encode()

        self.ser.write(message)

        if debug_param:
            print('Asked: ', message)
            print(len(payload))

        # time.sleep(2)

    def close(self):
        self.ser.close()     


class ArduinoResponse:
    def __init__(self, full_response=None, response_body=None, question_id=None, question_command=None, is_successful=True):
        self.response_body = response_body
        self.question_id = question_id
        self.command = question_command
        self.full_response = full_response

        self.successful = is_successful

    def split_response(self, save):
        splitted = self.full_response.split('*')

        if save:
            try:
                self.command = int(splitted[0])
                self.question_id = int(splitted[1])
                self.response_body = splitted[2]
            except IndexError:
                print('Response format is invalid!')

        return splitted

    def get_json_response(self, device_name, msg_type):
        # print(device_name + '$@' + self.response_body + '$@' + msg_type)
        return json.dumps({
            'device': device_name,
            'body': self.response_body,
            'type': msg_type,
        })
        # return device_name + '$@' + self.response_body + '$@' + msg_type

    def __str__(self):
        return f'Command: {self.command}, Body: {self.response_body}, Question id: {self.question_id}'


class SerialMonitor:
    def __init__(self, ard, con) -> None:
        self.ard = ard
        self.con = con
        self.t = None

    def on_msg(self, msg):
        print('New message from serial:', msg)
        r = ArduinoResponse(full_response=msg)
        r.split_response()
        self.con.send(r.get_json_response(spec.DEVICE_NAME, 'one'))

    def monitor(self, ard: Serial):
        while True:
            try:
                m = ard.readline().replace(b'\r\n', b'').decode('UTF-8')
                self.on_msg(m)
            except:
                break

    def start(self):
        self.t = threading.Thread(target=self.monitor, args=(self.ard, ))
        self.t.start()