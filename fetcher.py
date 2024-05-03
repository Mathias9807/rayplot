import datetime

import yfinance

# Dataframe: stores the trading data of one day. Stores day open price and each 1min close for the whole trading day
class Dataframe:
	def __init__(self, ticker: str, date: str, openPr: float, ticks: [float]):
		self.ticker = ticker
		self.date = date
		self.openPr = openPr
		self.ticks = ticks
		self.openTime = len(ticks) / 60

	def __str__(self):
		return '{} [{}]: open {}, ticks {}'.format(self.ticker, self.date, self.openPr, self.ticks)

dayCache = dict()

def getDay(ticker: str, date: str):
	if date in dayCache:
		return dayCache[date]

	stock = yfinance.Ticker(ticker)
	dayAfter = datetime.date.fromisoformat(date) + datetime.timedelta(days=1)
	data = stock.history(interval='1m', start=date, end=dayAfter)

	if len(data['Open']) > 0:
		return Dataframe(ticker, date, list(data['Open'])[0], list(data['Close']))
	else:
		return None

