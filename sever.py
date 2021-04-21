from flask import Flask, jsonify, request, render_template
import requests
import mysql.connector
import time
from datetime import datetime

#create table test(id int not null auto_increment, datetime varchar(50), status varchar(50), primary key (id));
#insert into test(datetime, status) values('gg', 'what');
db = mysql.connector.connect(
        host = "localhost",
        user = "mochis",
        passwd = "mochis",
        database = "aws")

mycursor = db.cursor()

app = Flask(__name__)

# receive post action from breadboard and return response
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
        return jsonify({'Home':'pimochis'})


# query database-HTML
@app.route('/html', methods=['GET'])
def get_html_table():
    mycursor.execute("select * from test")
    reg_data = mycursor.fetchall()
    return render_template('maria.html', data=reg_data)

# query database-JSON
@app.route('/json', methods=['GET'])
def get_json():
    mycursor.execute("select * from test")
    reg_data = mycursor.fetchall()
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
