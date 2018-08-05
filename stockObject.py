

class stockObject(object):
	"Object class for a stock"

	def __init__(self, ticker, data):
		self.ticker = ticker
		self.data = data

	@property
	def stock_ticker(self):
		return self.ticker
