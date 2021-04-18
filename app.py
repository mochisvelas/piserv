from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set pin 21 as output
GPIO.setup(21, GPIO.OUT)
# Turn off pin 21
GPIO.outpu(21, False)

@app.route('/on')
def on():
    GPIO.output(21, True)
    return render_template('on.html')

@app.route('/off')
def off():
    GPIO.output(21, False)
    return render_template('off.html')
