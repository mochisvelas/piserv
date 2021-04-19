import requests
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

def post_to_server(payload):
    r = requests.post('http://18.191.96.254:8080/', json=payload)
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
