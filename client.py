import requests
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

def post_to_server(payload):
    r = requests.post('http://18.220.62.23:8080/', json=payload)
    j = r.json().keys()
    print(r.json())
    GPIO.output(j[0], r.json()[j[0]])
    # if r.json()['21'] == '1':
    #     GPIO.output(21, True)
    # else:
    #     GPIO.output(21, False)
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
