from flask import Flask, jsonify, request, render_template
import requests
import pymongo
import time
from datetime import datetime

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['final']
picol = mydb['picol']
webcol = mydb['webcol']

# Get document id in string format
def get_data(data):
    data['_id'] = str(data['_id'])
    return data

# Get last mongo collection document
def get_last_doc(col):
    try:
        last_doc = col.find().sort([('_id', -1)]).limit(1)[0]
    except:
        last_doc = 'error'

    return last_doc

# Get display combination for raspi
def get_display(num):
    display = '0000000'
    if num == 0:
        display = '1111110'
    elif num == 1:
        display = '0110000'
    elif num == 2:
        display = '1101101'
    elif num == 3:
        display = '1111001'
    elif num == 4:
        display = '0110011'
    elif num == 5:
        display = '1011011'
    elif num == 6:
        display = '1011111'
    elif num == 7:
        display = '1110000'
    elif num == 8:
        display = '1111111'
    else:
        display = '1110011'

    return display

# receive post action from breadboard and return response based on html page
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):

        # update picol with lastest raspi post
        try:
            pi_json = request.get_json()
            pipost = pi_json['pival']
            piwait = pi_json['wait']
        except:
            pipost = 'pipost_error'
            piwait = 'piwait_error'
            print('cannot get pi_json')
        picol.insert_one({'pival':str(pipost)})

        if piwait == '1':
            # Wait until form() updates webcol
            aux_doc = get_last_doc(webcol)
            while True:
                last_doc = get_last_doc(webcol)
                try:
                    if last_doc['_id'] != aux_doc['_id']:
                        break
                except:
                    print('cannot get last_doc')

        ### DO SOMETHING WITH BOTH RASPI AND WEB POSTS ###
        ### DO SOMETHING WITH BOTH RASPI AND WEB POSTS ###
        ### DO SOMETHING WITH BOTH RASPI AND WEB POSTS ###
        ### DO SOMETHING WITH BOTH RASPI AND WEB POSTS ###

        return jsonify({'display':pipost}), 201

    else:
        #return if GET
        return jsonify({'Hello':'pimochis'})

# receive post action from html page, insert to db and return response
@app.route("/form", methods=['GET', 'POST'])
def form():
    # get last picol document
    try:
        last_pipost = picol.find().sort([('_id', -1)]).limit(1)[0]['pival']
    except:
        last_pipost = 'error'
        print('cannot get last_pipost')

    if(request.method == 'POST'):
        # get and insert input into webcol
        webpost = request.form.get('inputval')
        webcheck = 'False'
        if request.form.get('inputcheck'):
            webcheck = 'True'
        #webcheck = request.form.get('inputcheck')
        print(webcheck)
        webcol.insert_one({'webval':webpost, 'webcheck':webcheck})
        return render_template('final.html', data=last_pipost)
    else:
        # get form with last_pipost
        return render_template('final.html', data=last_pipost)

# query webcol-JSON
@app.route('/webson', methods=['GET'])
def get_webson():
    reg_data = [get_data(i) for i in webcol.find()]
    return jsonify(reg_data)

# query picol-JSON
@app.route('/pison', methods=['GET'])
def get_pison():
    reg_data = [get_data(i) for i in picol.find()]
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
