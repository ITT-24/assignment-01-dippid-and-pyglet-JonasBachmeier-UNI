import socket
import time
import random
import json
import math


IP = '127.0.0.1'
PORT = 5700

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.connect((IP,PORT))

counter = 0
while True:
    # Convert counter to a sinsu value with radius
    sinus = math.sin(math.radians(counter))

    # simulate DIPPID message as json
    msg = {
        'button_1': random.randint(0,1),
        'accelerometer': { 'x': sinus, 'y': sinus, 'z': sinus },
        }
    
    # send message to DIPPID-receiver.py
    server.sendto(json.dumps(msg).encode(), (IP,PORT))

    #increase / reset counter when 360°
    if counter != 360:
        counter += 1
    else:
        counter = 0

        
    time.sleep(1)
