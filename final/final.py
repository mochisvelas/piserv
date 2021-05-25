from flask import Flask, jsonify, request, render_template
import requests
import pymongo
import time

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['final']
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

# Get morse code
def get_morse(decimal):

    total = ''
    for num in decimal:
        if num == 0:
            morse = '11111'
        elif num == 1:
            morse = '01111'
        elif num == 2:
            morse = '00111'
        elif num == 3:
            morse = '00011'
        elif num == 4:
            morse = '00001'
        elif num == 5:
            morse = '00000'
        elif num == 6:
            morse = '10000'
        elif num == 7:
            morse = '11000'
        elif num == 8:
            morse = '11100'
        else:
            morse = '11110'

        total = total + morse 

    return total

# receive get action from pi and return response based on form page
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'GET'):
        # Wait until form() updates webcol
        aux_doc = get_last_doc(webcol)
        while True:
            last_doc = get_last_doc(webcol)
            try:
                if last_doc['_id'] != aux_doc['_id']:
                    break
            except:
                print('cannot get last_doc')

        last_doc = get_last_doc(webcol)
        decimal = last_doc['decimal']
        morse = get_morse(decimal)
        return jsonify({'morse':morse})

# receive post action from html page, insert to db and return response
@app.route("/form", methods=['GET', 'POST'])
def form():

    if(request.method == 'POST'):
        # get and insert input into webcol
        webpost = request.form.get('inputval')
        #if len(webpost) > 10:
        #    last_webpost = 'input is longer than 10'
        #    return render_template('final.html', data=last_webpost)
        #elif webpost.isdigit():
        #    last_webpost = 'has letters'
        #    return render_template('final.html', data=last_webpost)

        webcol.insert_one({'decimal':webpost})
        # get last webcol document
        try:
            last_webpost = webcol.find().sort([('_id', -1)]).limit(1)[0]['decimal']
        except:
            last_webpost = 'error'
            print('cannot get last_webpost')

        return render_template('final.html', data=last_webpost)
    else:
        # get form with last_webpost
        try:
            last_webpost = webcol.find().sort([('_id', -1)]).limit(1)[0]['decimal']
        except:
            last_webpost = 'error'
            print('cannot get last_webpost')
        return render_template('final.html', data=last_webpost)

# query webcol-JSON
@app.route('/webson', methods=['GET'])
def get_webson():
    reg_data = [get_data(i) for i in webcol.find()]
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
