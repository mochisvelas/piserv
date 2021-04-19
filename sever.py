from flask import Flask, jsonify, request, render_template
import requests
import mysql.connector
import time
from datetime import datetime
from json2html import * 

#create table test(id int not null auto_increment, datetime varchar(50), status varchar(50), primary key (id));
#insert into test(datetime, status) values('gg', 'what');
db = mysql.connector.connect(
        host = "localhost",
        user = "mochis",
        passwd = "mochis",
        database = "aws")

mycursor = db.cursor()

app = Flask(__name__)

# post action from breadboard and expect a response
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()
        now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if pi_json['20'] == '1':
            # insert reg in database
            mycursor.execute("insert into test(datetime, status) values('{}', 'on');".format(str(now)))
            db.commit()
            return jsonify({'21':'True'}), 201
        else:
            # insert reg in database
            mycursor.execute("insert into test(datetime, status) values('{}', 'on');".format(str(now)))
            db.commit()
            return jsonify({'21':'False'}), 201
    else:
        return jsonify({'about':'Hello pimochis'})

### WOULD HAVE TO MAKE THE PI A MINI SERVER??
# turn on pin 21 of raspi with phone
# @app.route('/on', methods=['GET', 'POST'])
# def on_off_pin():
#     if(request.method == 'POST'):
#         pi_json = request.get_json()
#         return jsonify({'21':'on'}), 201

# # turn off pin 21 of raspi with phone
# @app.route('/off', methods=['GET', 'POST'])
# def on_off_pin():
#     if(request.method == 'POST'):
#         pi_json = request.get_json()
#         return jsonify({'21':'off'}), 201
    
# # turn on/off pin with phone
# @app.route('/<int:pin>/<string:energy>', methods=['GET', 'POST'])
# def on_off_pin(pin, energy):
#     if(request.method == 'POST'):
#         pi_json = request.get_json()
#         return jsonify({str(pin): str(energy)}), 201

# query database
#@app.route('/input/<int:pin>/<string:energy>', methods=['GET'])
#def get_input_pin(pin, energy):
#    return jsonify({str(pin): str(energy)})

# query database-HTML
@app.route('/maria', methods=['GET'])
def get_html_table():
    data_all = []
    mycursor.execute("select * from test")
    for i in mycursor:
        data_all.append({'id':i[0], 'datetime':i[1], 'status':i[2]})
    columnNames = ['id', 'datetime', 'status']
    return render_template('maria.html', records=data_all, colnames=columnNames)

# query database-JSON
@app.route('/json', methods=['GET'])
def get_json():
    data_all = []
    mycursor.execute("select * from test")
    for i in mycursor:
        data_all.append({'id':i[0], 'datetime':i[1], 'status':i[2]})
    return jsonify(data_all)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
