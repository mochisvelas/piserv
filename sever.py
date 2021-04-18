from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

# post action from breadboard and expect a response
@app.route("/", methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        pi_json = request.get_json()
        if pi_json['20']:
            # insert reg in database
            return jsonify({'21':'on'}), 201
        else:
            # insert reg in database
            return jsonify({'21':'off'}), 201
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
@app.route('/input/<int:pin>/<string:energy>', methods=['GET'])
def get_input_pin(pin, energy):
    return jsonify({str(pin): str(energy)})

if __name__ == '__main__':
    app.run(debug=True)
