from flask import Flask, jsonify, request, render_template
import requests
import pymongo
import time
from datetime import datetime

#post = {"_id":2, "name":"eli"}

#while True:
#    mycol.insert_one({'name':'nobody'})
#    print('reg inserted')
#    time.sleep(3)

#mycol.insert_one(post)
#mycol.insert_one(post)

#res = mycol.find({"name":"Brenner"})
#res = mycol.find({})


#for r in res:
#    print(r)

# MONGO
client = pymongo.MongoClient()

mydb = client['testdb']
mycol = mydb['testcol']

def get_data(data):
     data['_id'] = str(data['_id'])
     return data

app = Flask(__name__)

# receive post action from breadboard and return response
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()
        now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if pi_json['20'] == '1':
            # insert reg in database
            mycol.insert_one({'datetime':now, 'status':'on'})
            return jsonify({'21':'True'}), 201
        else:
            # insert reg in database
            mycol.insert_one({'datetime':now, 'status':'off'})
            return jsonify({'21':'False'}), 201
    else:
        reg_data = [get_data(i) for i in mycol.find()]
        return render_template('main.html', data=reg_data)


# query database-HTML
@app.route('/html', methods=['GET'])
def get_html_table():
    reg_data = [get_data(i) for i in mycol.find()]
    return render_template('mongo.html', data=reg_data)

# query database-JSON
@app.route('/json', methods=['GET'])
def get_json():
    reg_data = [get_data(i) for i in mycol.find()]
    return jsonify(reg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
