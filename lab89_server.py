from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# receive post action from breadboard and return response
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()
        #binary = '11110010'
        if pi_json['20'] == '1':
            print('Insert binary number:')
            binary = input()
            return jsonify({'display': binary}), 201
        else:
            return jsonify({'display': binary}), 201
    else:
        return jsonify({'Home':'pimochis'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
