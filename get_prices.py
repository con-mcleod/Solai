#!/usr/bin/python3

import requests 

def get_response(datatype, ticker, interval):
	"""
	Function to request data from Alpha Vantage via API call
	:param datatype: the requested financial data type
	:param ticker: the requested company's stock ticker
	:param interval: the requested interval between stock prices
	:return: Python dictionary 
	"""

	session = requests.Session()
	session.max_redirects = 3
	
	url = "https://www.alphavantage.co/query"
	api_key = open('files/.api_key_get_prices').read()
	api_symbol = str(ticker)
	api_interval= str(interval)		# this is currently hardcoded to 60 min (1/5/15/30/60 exist)
	api_outputSize = "compact"

	if datatype == "Hourly":
		api_fn = "TIME_SERIES_INTRADAY"
	elif datatype == "Daily":
		api_fn = "TIME_SERIES_DAILY"
	elif datatype == "Adjusted Daily":
		api_fn = "TIME_SERIES_DAILY_ADJUSTED"
	# elif datatype == "FX":
	# 	api_fn = "CURRENCY_EXCHANGE_RATE"
	# 	from_currency = str(input("From currency? e.g. AUD\n"))
	# 	to_currency = str(input("To currency? e.g. USD\n"))
	# 	data = {
	# 		"function": api_fn,
	# 		"apikey": api_key,
	# 		"from_currency": from_currency,
	# 		"to_currency": to_currency
	# 	}


	data = {
		"function": api_fn,
		"symbol": api_symbol,
		"apikey": api_key,
		"interval": api_interval,
		"outputsize": api_outputSize
	}

	response = requests.get(url, params=data)
	return response
