from flask import Flask, jsonify, request, render_template
import requests
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['testdb']
mycol = mydb['testcol']

def get_data(data):
     data['_id'] = str(data['_id'])
     return data

# receive post action from breadboard and return response
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()
        if pi_json['20'] == '1':
            reg_data = ''
            last_reg = ''
            reg_data = [get_data(i) for i in mycol.find()]
            aux_reg = reg_data[-1]['_id']
            last_reg = ''
            while True:
                reg_data = [get_data(i) for i in mycol.find()]
                last_reg = reg_data[-1]
                if last_reg['_id'] != aux_reg:
                    break
                
            return jsonify({'new_status': str(last_reg['status'])}), 201
        else:
            return jsonify({'display': binary}), 201
    else:
        return jsonify({'Home':'pimochis'})

# receive post action from breadboard and return response
@app.route("/form", methods=['GET', 'POST'])
def form():
    if(request.method == 'POST'):
        status = request.form.get("onoff")
        print(str(status))
        mycol.insert_one({'status':status})
        return jsonify({'display': status}), 201
	#return
    else:
        return render_template('pre10.html')
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
