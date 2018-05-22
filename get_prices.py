#!/usr/bin/python3

import requests, json, sys

def get_response(datatype, interval, ticker):

	session = requests.Session()
	session.max_redirects = 3
	
	api_key = "3CR2W3WZA8NW8V9B"
	url = "https://www.alphavantage.co/query"

	if datatype == "Intraday":
		api_fn = "TIME_SERIES_INTRADAY"
	elif datatype == "Daily":
		api_fn = "TIME_SERIES_DAILY"
	elif datatype == "Adjusted Daily":
		api_fn = "TIME_SERIES_DAILY_ADJUSTED"
	elif datatype == "FX":
		api_fn = "CURRENCY_EXCHANGE_RATE"

	api_symbol = str(ticker)
	api_interval = str(interval)
	api_outputSize = "compact"

	data = {
		"function": api_fn,
		"symbol": api_symbol,
		"apikey": api_key,
		"interval": api_interval,
		"outputsize": api_outputSize
	}

	response = requests.get(url, params=data)
	return response


# elif datatype == "fx":
# 	api_fn = "CURRENCY_EXCHANGE_RATE"
# 	from_currency = str(input("From currency? e.g. AUD\n"))
# 	to_currency = str(input("To currency? e.g. USD\n"))

# 	data = {
# 		"function": api_fn,
# 		"apikey": api_key,
# 		"from_currency": from_currency,
# 		"to_currency": to_currency
# 	}