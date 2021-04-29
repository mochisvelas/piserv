from flask import Flask, jsonify, request, render_template
import requests
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['lab10']
pinarycol = mydb['pinary']
webimalcol = mydb['webimal']

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

        # update pinary collection with lastest raspi post
        pi_json = request.get_json()
        pinary = pi_json['pinary']
        pinarycol.insert_one({'pinary':str(pinary)})

        # Wait until form() updates webimal
        aux_reg = get_last_reg(webimalcol)
        while True:
            last_reg = get_last_reg(webimalcol)
            #print('pi is waiting')
            if last_reg['_id'] != aux_reg['_id']:
                break


        pinary2decimal = int(pinary, 2)
        total_decimal = pinary2decimal - int(last_reg['webimal'])

        display = '00000000'

        if total_decimal >= 10:
                units = total_decimal - 10
                display = get_display(units)
                display = display + '1'

        else:
                display = get_display(total_decimal)
                display = display + '0'


        return jsonify({'display':display, 'decimal':total_decimal, 'active':'True'}), 201

    else:
        #return if GET
        return jsonify({'Hello':'pimochis'})

# receive post action from html page, insert to db and return response
@app.route("/form", methods=['GET', 'POST'])
def form():
    if(request.method == 'POST'):
	# get and  insert decimal into webimal collection
        webimal = request.form.get("inputval")
        webimalcol.insert_one({'webimal':webimal})

	# show last pinary document
        last_pinary = pinarycol.find().sort([('_id', -1)]).limit(1)[0]['pinary']
        return render_template('lab10.html', data=last_pinary)
    else:
	# show last pinary document
        last_pinary = pinarycol.find().sort([('_id', -1)]).limit(1)[0]['pinary']
        return render_template('lab10.html', data=last_pinary)

# query database-JSON
@app.route('/json', methods=['GET'])
def get_json():
    reg_data = [get_data(i) for i in webimal.find()]
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
