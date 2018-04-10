#!/usr/bin/env python
from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import random
import main
import os
import datetime

with open('NYSE.csv') as f:
    listStock = list(csv.reader(f))

LISTOFSTOCKS = [e[0] for e in listStock if len(str(e[0])) > 2]

app = Flask(__name__, static_url_path='/static')

@app.route('/<stock>/<position>', methods=['POST', "GET"])
def mainStock(stock, position):
	stockTicker = stock.lower()
	price = float(main.getDifference(stock)) * 1000
	if price < 0:
		priceType = "Underpriced"
	else:
		priceType = "Overpriced"

	if position == "short" and priceType == "Underpricde":
		profitable = "False"
	if position == "short" and priceType == "Overpriced":
		profitable = "True"
	if position == "long" and priceType == "Underpriced":
		profitable = "True"
	if position == "long" and priceType == "Overpriced":
		profitable = "False"
	price = '${:,.2f}'.format(price)
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	currentHour = datetime.datetime.now().hour
	currentMinute = datetime.datetime.now().minute
	if currentHour > 7 and currentMinute > 29 and currentHour < 16 and datetime.datetime.today().weekday() < 5:
		openHours = "open"
	else:
		openHours = "closed"
	return render_template('index.html', stock=stock, position=position, stockTicker=stockTicker, profit=price, profitable=profitable, priceType=priceType, currentTime=time, openHours=openHours)


@app.route('/', methods=['POST', "GET"])
def genStock():
	stock = random.choice(LISTOFSTOCKS)
	return redirect(url_for('mainStock', stock=stock, position='long'))


@app.route('/calc/', methods=['POST'])
def genTrade(stock=False, position=False):
	results = list(request.form.items())
	if 'Short' in str(results):
		position = 'short'
	else:
		position = 'long'
	print(results)
	a = []
	for e in results:
		if "Ticker" in str(e):
			a.append(e)
	a.append(e)
	results = a
	stock = list(results)[0][1]
	for e in results:
		print(e)
	return redirect(url_for('mainStock', stock=stock, position=position))
	#return "It looks like you want to {} {}".format(position, stock)


@app.route('/trades/<ticker>', methods=['POST', "GET"])
def showTrades(ticker):
	return str(ticker)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
