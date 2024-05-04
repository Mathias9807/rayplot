import datetime
import copy
import pickle

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

cache = dict()
cacheFile = '/tmp/rayplot.cache'
def writeCache():
	processedFile = copy.deepcopy(cache)

	# Store all ticks as promille integers
	for ticker in processedFile:
		for date in processedFile[ticker]:
			processedFile[ticker][date].ticks = [round(tick * 1000) for tick in processedFile[ticker][date].ticks]

	with open(cacheFile, 'wb') as file:
		pickle.dump(processedFile, file)

# Populate cache if a cache file exists
try:
	with open(cacheFile, 'rb') as file:
		cache = pickle.load(file)

		for ticker in cache:
			for date in cache[ticker]:
				cache[ticker][date].ticks = [float(tick) / 1000 for tick in cache[ticker][date].ticks]
except FileNotFoundError:
	print('No stock cache found')

def getDay(ticker: str, date: str):
	if ticker in cache and date in cache[ticker]:
		return cache[ticker][date]

	stock = yfinance.Ticker(ticker)
	day = datetime.date.fromisoformat(date)
	dayAfter = day + datetime.timedelta(days=1)
	data = stock.history(interval='1m', start=date, end=dayAfter)

	if len(data['Open']) > 0:
		df = Dataframe(ticker, date, list(data['Open'])[0], list(data['Close']))

		# Save to cache if it's data for a previous day
		if day < datetime.date.today():
			if ticker not in cache:
				cache[ticker] = dict()
			cache[ticker][date] = df
			writeCache()
			print('Saved [{} {}] to cache'.format(ticker, date))

		return df
	else:
		return None

