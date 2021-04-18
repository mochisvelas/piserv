import requests
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

while True:
    if GPIO.input(20):
        payload = {'20':'1'}
        r = requests.post('http://127.0.0.1:5000/', json=payload)

        if r.json()['21'] == '1':
            GPIO.output(21, True)
        else:
            GPIO.output(21, False)

GPIO.cleanup()
