import requests
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(0, GPIO.OUT) # DISPLAY A
GPIO.setup(1, GPIO.OUT) # DISPLAY B
GPIO.setup(7, GPIO.OUT) # DISPLAY C
GPIO.setup(8, GPIO.OUT) # DISPLAY D
GPIO.setup(4, GPIO.OUT) # DISPLAY E
GPIO.setup(5, GPIO.OUT) # DISPLAY F
GPIO.setup(6, GPIO.OUT) # DISPLAY G
GPIO.setup(9, GPIO.OUT) # RELAY
GPIO.setup(20, GPIO.IN) # SWITCH

def post_to_server(payload):
    ip = 'http://18.224.139.147:8080/'
    r = requests.post(ip, json=payload)
    binary = r.json()['display']
    GPIO.output(0, binary[0] == '1')
    GPIO.output(1, binary[1] == '1')
    GPIO.output(7, binary[2] == '1')
    GPIO.output(8, binary[3] == '1')
    GPIO.output(4, binary[4] == '1')
    GPIO.output(5, binary[5] == '1')
    GPIO.output(6, binary[6] == '1')
    GPIO.output(9, binary[7] == '1')
    return

while True:

    if GPIO.input(20):
        payload = {'20':'1'}
        post_to_server(payload)
        while GPIO.input(20):
            continue
    else:
        while not GPIO.input(20):
            continue

GPIO.cleanup()
