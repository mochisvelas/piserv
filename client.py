import requests
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

def post_to_server(payload):
    ip = 'http://18.224.139.147:8080/'
    r = requests.post(ip, json=payload)
    j = r.json()
    k = list(j)
    GPIO.output(int(k[0]), j[k[0]] == 'True')
    return

while True:

    if GPIO.input(20):
        payload = {'20':'1'}
        post_to_server(payload)
        while GPIO.input(20):
            continue
    else:
        payload = {'20':'0'}
        post_to_server(payload)
        while not GPIO.input(20):
            continue

GPIO.cleanup()
