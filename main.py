import requests
import bs4
import subprocess
import json
 


proxies = {}
email = ''
password = ''

def get_value(stock):
	get_value_url = 'http://finance.google.com/finance/info?client=ig&q=' + stock
	value = subprocess.Popen(['curl', '-s', get_value_url], stdout=subprocess.PIPE).communicate()[0]
	j = json.loads(value[5:len(value)-2])
	return float(j['l'])
 
def MakeTrade(stock, quantity):
	s = requests.Session()
	data = {'form_id':'account_api_form', 'email': email,
	'password': password, 'op': 'Sign In'}
	url = 'http://www.investopedia.com/accounts/login.aspx'
	r = s.post(url, data=data, proxies=proxies)
	r = s.get('http://www.investopedia.com/simulator/portfolio/?gameid=342', data=data, proxies=proxies)
	soup = bs4.BeautifulSoup(r.text, 'lxml')
	AccountValue = soup.select('#ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue')[0].getText()
	r = s.post('http://www.investopedia.com/simulator/ajax/quotebox.aspx', data={'symbol': "AAPL"})
	r = s.get('http://www.investopedia.com/simulator/trade/tradestock.aspx')
	page = bs4.BeautifulSoup(r.text, 'lxml')
	for e in page.find_all("input", type="hidden"):
		if "formToken" in str(e):
			Form_ID = str(e).partition('type="hidden" value="')[2].partition('"/>')[0]
	ticker = raw_input('ticker')
	quantity = raw_input('quantity')
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
			print(Form_ID)
	urltoken = str(r.url).partition('&urlToken=')[2]
	data = {'submitOrder':'Submit+Order+%3E%3E', 'formToken': Form_ID}
	url = 'http://www.investopedia.com/simulator/trade/tradestockpreview.aspx?too=1&type=1&Sym={}&Qty={}&lmt=0&do=2&em=true&urlName=simTrade2Preview&urlToken={}'.format(ticker, quantity, urltoken)
	res = s.post(url, data=data)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print('Purchased {} Shares of {}'.format(quantity, stock))