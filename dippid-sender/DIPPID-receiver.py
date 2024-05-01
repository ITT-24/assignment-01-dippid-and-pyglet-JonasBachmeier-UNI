import socket
import time
import json


IP = '127.0.0.1'
PORT = 5700

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP,PORT))

while True:

    # receive message from DIPPID-sender.py
    recv = server.recv(9999)

    # try to decode message by loading json
    try:
        message = json.loads(recv.decode())
        print(message)

        # check if button_1 is pressed
        if message['button_1']:
            print("Button 1 pressed")

    # if message isn't json just print received msg
    except json.JSONDecodeError:
        print("Not JSON: ", recv.decode())
    time.sleep(1)

