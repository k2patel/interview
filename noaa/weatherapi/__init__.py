
from flask import Flask, jsonify, Response, request, g
import os, sys, json
from datetime import datetime
from importlib import import_module
# from get_from_noaa import noaa
import requests

# create and configure the app
app = Flask(__name__)
app.config.from_pyfile('config.py')
# app.config['CDO_TOKEN'] = "CDO_TOKEN"
# app.config.from_object('config')
# Override if evironment has variable defined.
#app.config.from_envvar('CDO_TOKEN')

@app.before_request
def before_request():
    g.request_start_time = datetime.now().astimezone().replace(microsecond=0).isoformat()

def convert_FIPS(state):
    try:
        response = requests.get('https://coastwatch.pfeg.noaa.gov/erddap/convert/fipscounty.txt?county=' + state)
        if response.ok:
            return str(response.text)
        else:
            return False
    except IOError:
        return False

def noaa(state, CDO_TOKEN):
    fips_id_full = convert_FIPS(state)
    fips_id = fips_id_full.rstrip("0")
    url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:'+fips_id
    try:
        if fips_id:
            response = requests.get(url, headers = {'token': CDO_TOKEN})
            if response.ok:
                parsed = json.loads(response.text)
                mDictionary = { "requestTime":g.request_start_time, "responseTime":datetime.now().astimezone().replace(microsecond=0).isoformat(), "state":state, "results":parsed['metadata']['resultset']['count'], "offset":parsed['metadata']['resultset']['offset'], "limit":parsed['metadata']['resultset']['limit'] }
                mDictionary.update({"stations":parsed['results']})
                serialized = json.dumps(mDictionary, sort_keys=False, indent=4)
                return serialized
            else:
                return False
    except IOError:
        return False

@app.route('/station', methods=['post'])
def index():
    state = request.args.get('state', '')
    output = noaa(state=state, CDO_TOKEN=app.config['CDO_TOKEN'])
    resp = Response(output)
    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return resp