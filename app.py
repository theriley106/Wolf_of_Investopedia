from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import random
import os

LISTOFSTOCKS = ["TSLA", "AAPL", "GOOG"]

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', "GET"])
def song():
	return render_template('index.html')

@app.route('/calc/', methods=['POST'])
def genTrade(stock=False, position=False):
	for values in list(request.form.items()):
		if str(values[1]).upper() in LISTOFSTOCKS:
			stock = str(values[1]).upper()
		if "Short" in str(values):
			position = "Short"
		if "Long" in str(values):
			position = "Long"
	if stock == False:
		stock = random.choice(LISTOFSTOCKS)
	if position == False:
		position = random.choice(["Long", "Short"])
	
	return "It looks like you want to {} {}".format(position, stock)


@app.route('/trades/<ticker>', methods=['POST', "GET"])
def showTrades(ticker):
	return str(ticker)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
