#!/usr/bin/python3

class stockObject(object):
	"""
	Object class for a stock
	"""

	def __init__(self, ticker, data):
		"""
		Initialise the object
		:param ticker: the stock's identifying ticker
		:param data: a Python object containing stock price information
		"""
		self.ticker = ticker
		self.data = data

	@property
	def stock_ticker(self):
		return self.ticker

	@property
	def stock_data(self):
		return self._stock_data
	