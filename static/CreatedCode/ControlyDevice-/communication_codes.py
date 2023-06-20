# ! All communication codes for communication between arduino and pc over serial communication

CODE = {
    'yes': 1,
    'no': 0,
    'ask_for_changes': 2,
    'sending_changes': 3,
    # 'ask_for_status': 4
}

WAIT_TIMES = {
    'low': 0.01,
    'medium': 0.1,
    'high': 2,
}
# ! Wait Time Legend:
# ? You can try increasing baud rate
# ~ low = 100 bits
# ~ medium = 960 bits
# ~ high = 9600 bits
