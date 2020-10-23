import requests
import bs4
import subprocess
import csv
import random
import os
import json
import time
import re
from selenium import webdriver


proxies = {}
email = ''
password = ''

def grabStocks(csvfile):
    return [line.split()[0] for line in open(csvfile)]


class getQuotes(object):
	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		self.driver = webdriver.PhantomJS()
		self.driver.get('http://www.investopedia.com/markets/stocks/tsla/')
		self.driver.save_screenshot('screen.png') # save a screenshot to disk
		networkActivity = str(re.findall('https:\/\/superquotes\.xignite\.com\/((.*?))"', str(self.driver.get_log('har')))[0])
		self.Token = str(networkActivity.partition("&_token=")[2]).partition('&')[0]
		self.UserID = ''.join(re.findall('(\d+)\D', str(networkActivity.partition("&_token_userid=")[2].partition(' ')[0])))

	def getQuote(self, ticker):
		url = "https://superquotes.xignite.com/xSuperQuotes.json/GetQuotes?IdentifierType=Symbol&Identifiers={}&_token={}&_token_userid={}".format(ticker, self.Token, self.UserID)
		#self.driver.get(url)
		#print self.driver.page_source
		return (requests.get(url).text)
		#self.driver.get_cookies()

def get_real_value(stock):
	return requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&apikey=3ZC52BSRXYLK76YY'.format(stock)).json()

def extractChange(stock, minute=15):
	a = get_real_value(stock)
	a = sorted(a["Time Series (1min)"].items())[::-1]
	return [a[0], a[minute-1]]

def getDifference(stock, minute=15):
	a = extractChange(stock, minute)
	first = str(a[0]).partition('close')[2]
	value1 = float(re.findall('\d*\.\d*', first)[0])
	second = str(a[1]).partition('close')[2]
	value2 = float(re.findall('\d*\.\d*', second)[0])
	return float('{:,.2f}'.format(value1 - value2))

def get_value(stock):
	get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + stock
	value = subprocess.Popen(['curl', '-s', get_value_url], stdout=subprocess.PIPE).communicate()[0]
	j = json.loads(value[5:len(value)-2])
	return float(j['l'])
def getDiff(ticker):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	url = "https://www.google.com/finance/getprices?i=60&p=16m&f=d,o,h,l,c,v&df=cpct&q={}".format(ticker)
	res = requests.get(url, headers=headers)
	print(res.text)
	result = str(res.text).split('\n')[8:-1]
	result = [result[0], result[-1]]
	quoteone = float(re.findall('\d,(\d+\.\d+)', str(result[0]))[0])
	quotetwo = float(re.findall('\d,(\d+\.\d+)', str(result[1]))[0])
	return abs(quotetwo - quoteone)
	#print result

def MakeTrade(ticker, quantity, username, password):
	s = requests.Session()
	data = {'form_id':'account_api_form', 'email': username,
	'password': password, 'op': 'Sign In'}
	url = 'http://www.investopedia.com/accounts/login.aspx'
	r = s.post(url, data=data, proxies=proxies)
	r = s.get('http://www.investopedia.com/simulator/portfolio/', data=data, proxies=proxies)
	soup = bs4.BeautifulSoup(r.text, 'lxml')
	AccountValue = soup.select('p')[0].getText()
	r = s.post('http://www.investopedia.com/simulator/ajax/quotebox.aspx', data={'symbol': "AAPL"})
	r = s.get('http://www.investopedia.com/simulator/trade/tradestock.aspx')
	page = bs4.BeautifulSoup(r.text, 'lxml')
	for e in page.find_all("input", type="hidden"):
		if "formToken" in str(e):
			Form_ID = str(e).partition('type="hidden" value="')[2].partition('"/>')[0]
	data = {'formToken': str(Form_ID), 'symbolTextbox':ticker,
	'symbolTextbox_mi_1_value':'AAPL',
	'selectedValue':ticker,
	'transactionTypeDropDown':'1',
	'quantityTextbox':quantity,
	'isShowMax':'0',
	'Price':'Market',
	'limitPriceTextBox':'',
	'stopPriceTextBox':'',
	'tStopPRCTextBox':'',
	'tStopVALTextBox':'',
	'durationTypeDropDown':'2',
	'sendConfirmationEmailCheckBox':'on'}
	r = s.post('http://www.investopedia.com/simulator/trade/tradestock.aspx', data=data)
	page = bs4.BeautifulSoup(r.text, 'lxml')
	for e in page.find_all("input", type="hidden"):
		if "formToken" in str(e):
			Form_ID = str(e).partition('type="hidden" value="')[2].partition('"/>')[0]
	urltoken = str(r.url).partition('&urlToken=')[2]
	data = {'submitOrder':'Submit+Order+%3E%3E', 'formToken': Form_ID}
	url = 'http://www.investopedia.com/simulator/trade/tradestockpreview.aspx?too=1&type=1&Sym={}&Qty={}&lmt=0&do=2&em=true&urlName=simTrade2Preview&urlToken={}'.format(ticker, quantity, urltoken)
	res = s.post(url, data=data)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print('Purchased {} Shares of {}'.format(quantity, stock))

def calcDiff(stock):
	get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + stock
	value = subprocess.Popen(['curl', '-s', get_value_url], stdout=subprocess.PIPE).communicate()[0]
	j = json.loads(value[5:len(value)-2])
	first = float(j['l'])
	time.sleep(15*60)
	get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + stock
	value = subprocess.Popen(['curl', '-s', get_value_url], stdout=subprocess.PIPE).communicate()[0]
	j = json.loads(value[5:len(value)-2])
	return float((float(j['l']) - first) / float(first))

def genStocks(csvfile="src/companylist.csv"):
	stocksCSV = open(csvfile, 'r')
	stocklist = csv.reader(stocksCSV)
	stocklist = [row for row in stocklist]
	stocklist = [l[0] for l in stocklist]
	random.shuffle(stocklist)
	return stocklist

if __name__ == "__main__":
	a = getQuotes()
	e = []
	for t in grabStocks("NYSE.csv"):
		if "RequestError" in str(a.getQuote(t)):
			print("Error with {}".format(t))
		else:
			print("Good")
			e.append(t)
	e = list(set(e))
	with open('returns.csv', 'wb') as f:
		writer = csv.writer(f)
		for val in e:
			writer.writerow([val])
	for i in range(10):
		ticker = input("Ticker: ")
		ticker = str(ticker).upper()
		a.getQuote(ticker)
