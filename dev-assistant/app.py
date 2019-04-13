from flask import Flask, render_template, request, send_file, flash, redirect, session, abort, url_for

import os
from nlp.rasa import RasaNLP
from dataprovider.dataprovider import DataProvider
import traceback
import sys
import rasa_nlu
import json
from flask_cors import CORS
import time
import requests
from datetime import datetime, timedelta

from googleSearcher import google_search
from cveSearcher import cveSearcher

app = Flask(__name__)
CORS(app, support_credentials=True)

def getCommits(username, repository):
	import requests

	url = "https://api.github.com/repos/" + username + "/" + repository + "/commits"

	payload = ""
	headers = {
	    'cache-control': "no-cache",
	    'Postman-Token': "239f477a-cdb6-4bff-a265-3e487853b9c2"
	    }

	response = requests.request("GET", url, data=payload, headers=headers)

	return json.loads(response.text)

def process_msg(data, rasa_nlu):
	print("message received" + data)

	if (data.split(" ")[0]) == 'stackoverflow':
		queryForGoogle = ' '.join(data.split(" ")[1: ])
		print(queryForGoogle)
		searchResults = google_search(queryForGoogle)
		return 'stackoverflow', searchResults

	if (data.split(" ")[0]) == 'github':
		githubDetails = data.split(" ")[-1]
		return 'github', githubDetails

	if (data.split(" ")[0]) == 'reminder':
		reminderDetails = ' '.join(data.split(" ")[1:])
		return 'reminder', reminderDetails

	text_to_reply = rasa_nlu.find_reply(data, session)
	if text_to_reply:
		print(text_to_reply)
		return text_to_reply

@app.route('/old', methods=['GET', 'POST'])
def oldIndex():
	session['product'] = ''
	session['product_price'] = ''
	session['product_cod'] = ''
	session['product_discount'] = ''
	session['myDiscount'] = 0

	return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
	session['product'] = ''
	session['product_price'] = ''
	session['product_cod'] = ''
	session['product_discount'] = ''
	session['myDiscount'] = 0

	return render_template('chatbot.html')

@app.route('/best', methods=['GET', 'POST'])
def bestIndex():
	session['product'] = ''
	session['product_price'] = ''
	session['product_cod'] = ''
	session['product_discount'] = ''
	session['myDiscount'] = 0

	return render_template('best.html')

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
        
        return json.dumps(cveDetails[0])

    return 'alive'

@app.route('/api/check/cve', methods=['GET', 'POST'])
def cve():
    return 'success'

@app.route('/process', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		print(request.form)
		myPayload = request.form['chatInput']
		print('received at flask server : ' + myPayload)

		chatContext, chatReply = process_msg(myPayload, rasa_nlu)

		if chatContext == 'reminder':
			print(chatReply)
			return json.dumps({"context": "reminder", "reply": chatReply})

		if chatContext == 'stackoverflow':
			print(chatReply)
			print('---')
			return json.dumps({"context": "so", "reply": chatReply[:5]})

		if chatContext == 'github':
			username, repo = chatReply.split("/")
			commitJson = getCommits(username, repo)
			return json.dumps({"context": "github", "reply": commitJson})

		try:
			if chatContext[0] != session['product'] :
				session['myDiscount'] = 0

			session['product'] = ''
			session['product_price'] = ''
			session['product_cod'] = ''
			session['product_discount'] = ''

			if chatContext[0] != '' : session['product'] = chatContext[0]
			if chatContext[1] != '' : session['product_price'] = chatContext[1]
			if chatContext[2] != '' : session['product_cod'] = chatContext[2]
			if chatContext[3][0] != '' : session['product_discount'] = chatContext[3][0]

			if session['myDiscount'] == 0 : session['myDiscount'] = chatContext[3][1]

			return json.dumps({"context": "general", "reply": chatReply})

		except:
			return json.dumps({"context": "general", "reply": chatReply})

	return json.dumps({"context": "general", "reply": "Tricking me?"})


app.secret_key = "digital-assistant"

if __name__ == '__main__':

	try:
		dp = DataProvider(os.environ.get("RL222P-RT8L7JURJR"))
	
		r = RasaNLP(dp, "rasa-config.json", "./data/training_data.json", "./rasa-model")
		r.train()
	
		rasa_nlu = r

	except KeyboardInterrupt:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		sys.exit(0)
	except:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		traceback.print_exc()

	app.run(debug=True, threaded=True)