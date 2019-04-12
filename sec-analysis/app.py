from flask import Flask, render_template, request, send_file, flash, redirect, session, abort, url_for, jsonify
from flask_cors import CORS
import time
import json
import os
import requests

from cveSearcher import cveSearcher

app = Flask(__name__)
app.secret_key = 'redhatHack'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def index():
	return 'OK'

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    time.sleep(2)

    url = "https://www.jsonstore.io/d2a87b276883fef8b464807a65dc270bf21094ebae987ca5973c95880bd27f40"
    
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "c9d1e864-6e93-4ee4-a6f5-caaa69fa53ab"
        }
    
    response = requests.request("GET", url, data=payload, headers=headers)
    
    myCode = response.text
    codeJson = json.loads(myCode)
    codeLanguage = codeJson['result']['language']
    codeSource = codeJson['result']['code']

    fileName = './source.' + codeLanguage

    f = open(fileName, 'w')
    f.write(codeSource)
    f.close()
    print(fileName)

    if codeLanguage == 'Python':
        os.system("bandit " + fileName + " > bandit.results")
        f = open('bandit.results', 'r')

        cveDetails = []

        for line in f.readlines():
            if line.startswith('>>'):
                query = ' '.join(line.split(" ")[3: -1])[:-1]
                cveDetails = cveSearcher(query)
        
        print(cveDetails)

    return 'alive'

@app.route('/api/check/cve', methods=['GET', 'POST'])
def cve():
    return 'success'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)