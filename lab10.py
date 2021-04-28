from flask import Flask, jsonify, request, render_template
import requests
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['lab10']
pinarycol = mydb['pinary']
webimalcol = mydb['webimal']

active = False

# Get document id in string format
def get_data(data):
    data['_id'] = str(data['_id'])
    return data

# Get last mongo collection document
def get_last_reg(col):
    last_reg = col.find().sort([('_id', -1)]).limit(1)[0]
    return last_reg

# Get display combination for raspi
def get_display(num):
    display = '0000000'
    if num == 0:
        display = '1111110'
    elif num == 1:
        display = '0011000'
    elif num == 2:
        display = '1101101'
    elif num == 3:
        display = '0111101'
    elif num == 4:
        display = '0011011'
    elif num == 5:
        display = '0110111'
    elif num == 6:
        display = '1110111'
    elif num == 7:
        display = '0011100'
    elif num == 8:
        display = '1111111'
    else:
        display = '0011111'

    return display

# receive post action from breadboard and return response based on html page
@app.route("/", methods=['GET', 'POST'])
def index():

    global active

    if(request.method == 'POST'):

        # update pinary collection with lastest raspi post
        pi_json = request.get_json()
        pinary = pi_json['pinary']
        last_pinary = get_last_reg(pinarycol)
        if pinary != last_pinary['pinary']:
            pinarycol.insert_one({'pinary':pinary})

        #global active

        if not active:
            return jsonify({'active':'False'})

        pinary2decimal = int(pinary, 2)

        last_reg = get_last_reg(webimalcol)
        #aux_reg = get_last_reg(webimalcol)
        # Wait until form() updates webimal
        #while True:
        #    last_reg = get_last_reg(webimalcol)
        #    if last_reg['_id'] != aux_reg['_id']:
        #        break


        total_decimal = pinary2decimal - int(last_reg['webimal'])

        display = '00000000'

        if total_decimal >= 10:
                units = total_decimal - 10
                display = get_display(units)
                display = display + '1'

        else:
                display = get_display(total_decimal)
                display = display + '0'

        active = False

        return jsonify({'display':display, 'decimal':total_decimal, 'active':'True'}), 201

    else:
    #return if GET
        return jsonify({'Hello':'pimochis'})

# receive post action from html page, insert to db and return response
@app.route("/form", methods=['GET', 'POST'])
def form():

    global active

    if(request.method == 'POST'):
	# get and  insert decimal into webimal collection
        webimal = request.form.get("inputval")
        last_webimal = get_last_reg(webimalcol)
        if webimal != last_webimal['webimal']:
            webimalcol.insert_one({'webimal':webimal})

        last_pinary = pinarycol.find().sort([('_id', -1)]).limit(1)[0]['pinary']
        active = True
        return render_template('lab10.html', data=last_pinary)
    else:
	# show last pinary document
        last_pinary = pinarycol.find().sort([('_id', -1)]).limit(1)[0]['pinary']
        #print(last_pinary)
        return render_template('lab10.html', data=last_pinary)

# query database-JSON
@app.route('/json', methods=['GET'])
def get_json():
    reg_data = [get_data(i) for i in webimal.find()]
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
