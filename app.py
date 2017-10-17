from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import random
import os
import datetime
LISTOFSTOCKS = []
with open('NYSE.csv', 'rb') as f:
    reader = csv.reader(f)
    listStock = list(reader)

for e in listStock:
	if len(str(e[0])) > 2:
		LISTOFSTOCKS.append(e[0])

app = Flask(__name__, static_url_path='/static')

@app.route('/<stock>', methods=['POST', "GET"])
def mainStock(stock):
	stockTicker = stock.lower()
	return render_template('index.html', stock=stock, stockTicker=stockTicker, currentTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
	
@app.route('/', methods=['POST', "GET"])
def genStock():
	stock = random.choice(LISTOFSTOCKS)
	
	return redirect(url_for('mainStock', stock=stock))

@app.route('/calc/', methods=['POST'])
def genTrade(stock=False, position=False):
	a = []
	results = list(request.form.items())
	for e in results:
		if "Ticker" in str(e):
			a.append(e)
	a.append(e)
	results = a
	position = list(results)[1][0]
	stock = list(results)[0][1]
	for e in results:
		print e
	return redirect(url_for('mainStock', stock=stock))
	#return "It looks like you want to {} {}".format(position, stock)


@app.route('/trades/<ticker>', methods=['POST', "GET"])
def showTrades(ticker):
	return str(ticker)



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
