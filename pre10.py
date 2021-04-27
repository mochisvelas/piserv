from flask import Flask, jsonify, request, render_template
import requests
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient()

mydb = client['testdb']
mycol = mydb['testcol']

# Get document id in string format
def get_data(data):
    data['_id'] = str(data['_id'])
    return data

# Get last mongo collection document
def get_last_reg():
    last_reg = mycol.find().sort([('_id', -1)]).limit(1)[0]
    return last_reg

# receive post action from breadboard and return response based on html page
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()

        ## POSSIBLE LAB 10
        er_time = int(pi_json['er_time'])
        aux_reg = get_last_reg()

        # Wait until form() updates database
        while True:
            last_reg = get_last_reg()
            if last_reg['_id'] != aux_reg['_id']:
                break

        total_time = er_time * int(last_reg['form_time'])
        ## POSSIBLE LAB 10

        ## PREVIOUS LABS
        #if pi_json['20'] == '1':
        #    aux_reg = get_last_reg()

            # Wait until form() updates database
        #    while True:
        #        last_reg = get_last_reg()
        #        if last_reg['_id'] != aux_reg['_id']:
        #            break
        ## PREVIOUS LABS

        return jsonify({'total_time':total_time}), 201
        #else:
        #    return jsonify({'Pi sent': '0'}), 201

    #return if GET
    return jsonify({'Home':'pimochis'})

# receive post action from html page, insert to db and return response
@app.route("/form", methods=['GET', 'POST'])
def form():
    if(request.method == 'POST'):
        form_time = request.form.get("inputval")
        #print(str(status))
        mycol.insert_one({'form_time':form_time})
        return render_template('pre10.html')
    else:
        return render_template('pre10.html')
        
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
