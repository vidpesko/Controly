# Vid Pesko
# ! Every Controly Device will need this code
# ? Here is everything for a device to:
# * connect to arduino via serial communication
# * send data to arduino
# * receive data back from arduino

from communication_codes import CODE

from serial import Serial
import time
import json

# ! Animations
animations = {
    'basic': '0',
    'steps': '1',
}


class Arduino:
    def __init__(self, port) -> None:
        self.ser = Serial(baudrate=9600)
        self.ser.port = port
        self.state = 0

    def connect(self):
        self.ser.open()
        time.sleep(2)

    def ask_and_wait(self, code: int, question_id: int, payload: str = None, bool_param: bool = False, debug_param: bool = True):
        # question_id is used as fail-safe -> to check if question and answer match
        start_t = time.time() * 1000

        # Ask arduino
        payload = payload if payload is not None else 'empty_payload'
        message = str(code) + '*' + str(question_id) + '*' + payload
        message = message.encode('utf-8')

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        time.sleep(0.1)

        self.ser.write(message)

        if debug_param:
            print('Asked: ', message)

        time.sleep(0.1)

        full_response = self.ser.read_until().decode('utf-8').replace('\r\n', '')

        if debug_param:
            print('Got: ', full_response)
            print('Completed in [ milliseconds ]: ', (time.time() * 1000) - start_t)
            print()

        response = ArduinoResponse(full_response=full_response)
        response.split_response(save=True)

        time.sleep(0.1)

        if bool_param:
            return True if response.response_body == CODE['yes'] else False

        return response

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