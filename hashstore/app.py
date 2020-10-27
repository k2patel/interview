"""Flask API."""
from flask import Flask, jsonify, request
import requests, hashlib, os, logging
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info("app_info", "App Information", version="1.0.0")

def message_hash(message):
    hashval = hashlib.sha256(str(message).encode()).hexdigest()
    return str(hashval)

def msg_store(message):
    hashval = message_hash(message)
    cwd = os.getcwd()
    try:
        with open(cwd+'/data/'+hashval,'w') as f:
            f.write(message)
            f.close()
            return str(hashval)
    except IOError:
        return False

def chk_store(hashval):
    cwd = os.getcwd()
    try:
        with open(cwd+'/data/'+hashval, 'r') as f:
            hash_cont = f.read()
            return hash_cont
    except IOError:
        return False

@app.route('/')
def index():
    return "Hello, There is nothing here"

@app.route('/messages', methods=['POST'])
def message_index():
    if request.is_json:
        content = request.get_json()
        hashval = msg_store(content['message'])
        if hashval:
            return jsonify( {"digest": str(hashval)}), {'Content-Type': 'application/json'}
        else:
            return jsonify( {"error": "Failed to write"}), {'Content-Type': 'application/json'}
    else:
        return "Please provide JSON"


@app.route('/messages/<message>', methods=['GET'])
def message_retrive(message):
    content = chk_store(message)
    if content:
        return jsonify( {"message": str(content)})
    else:
        return jsonify( {"error": "unable to find message", "message_sha256": str(message)}), 404, {'Content-Type': 'application/json'}

@app.route('/path', methods=['GET'])
def path_loc():
    return str(os.getcwd())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
