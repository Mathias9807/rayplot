import datetime
import copy
import pickle

import yfinance

# Dataframe: stores the trading data of one day. Stores day open price and each 1min close for the whole trading day
class Dataframe:
	def __init__(self, ticker: str, date: str | datetime.date, historyData):
		self.ticker = ticker
		self.date = date
		self.openPr = list(historyData['Open'])[0]
		self.ticks = list(historyData['Close'])  # Actual per-minute data
		self.openTime = len(self.ticks) / 60  # Time in hours the security was traded for
		self.openHour = historyData.index[0].hour + historyData.index[0].minute / 60  # Hour at which market opened

	def getPreviousDay(self):
		if isinstance(self.date, datetime.date):
			date = self.date
		else:
			date = datetime.date.fromisoformat(self.date)
		while True:
			date -= datetime.timedelta(days=1)
			prev = getDay(self.ticker, date.strftime('%Y-%m-%d'))
			if prev is not None:
				return prev

	def __str__(self):
		return '{} [{}]: open {}, ticks {}'.format(self.ticker, self.date, self.openPr, self.ticks)

cache = dict()
cacheFile = '/tmp/rayplot.cache'
def writeCache():
	processedFile = copy.deepcopy(cache)

	# Store all ticks as promille integers
	for ticker in processedFile:
		for date in processedFile[ticker]:
			if processedFile[ticker][date] is not None:
				processedFile[ticker][date].ticks = [round(tick * 1000) for tick in processedFile[ticker][date].ticks]

	with open(cacheFile, 'wb') as file:
		pickle.dump(processedFile, file)

# Populate cache if a cache file exists
try:
	with open(cacheFile, 'rb') as file:
		cache = pickle.load(file)

		for ticker in cache:
			for date in cache[ticker]:
				if cache[ticker][date] is not None:
					cache[ticker][date].ticks = [float(tick) / 1000 for tick in cache[ticker][date].ticks]
except FileNotFoundError:
	print('No stock cache found')

def getDay(ticker: str, date: str | datetime.date):
	if ticker in cache and date in cache[ticker]:
		return cache[ticker][date]

	stock = yfinance.Ticker(ticker)
	if isinstance(date, datetime.date):
		day = date
	else:
		day = datetime.date.fromisoformat(date)
	dayAfter = day + datetime.timedelta(days=1)
	data = stock.history(interval='1m', start=date, end=dayAfter)

	if len(data['Open']) > 0:
		df = Dataframe(ticker, date, data)

		# Save to cache if it's data for a previous day
		if day < datetime.date.today():
			if ticker not in cache:
				cache[ticker] = dict()
			cache[ticker][date] = df
			writeCache()
			print('Saved [{} {}] to cache'.format(ticker, date))

		return df
	else:
		# Save empty days to cache so we don't waste time checking again
		if day < datetime.date.today():
			if ticker not in cache:
				cache[ticker] = dict()
			cache[ticker][date] = None
			writeCache()
		return None

def getDataSeries(ticker: str, startDate: str, endDate: str) -> [Dataframe]:
	series = []

	date = datetime.date.fromisoformat(startDate)
	endDate = datetime.date.fromisoformat(endDate)
	while date <= endDate:
		df = getDay(ticker, date.strftime('%Y-%m-%d'))
		if df is not None:
			series.append(df)
		date += datetime.timedelta(days=1)

	return series

def getDataSeriesUpTo(ticker: str, endDate: str | datetime.date, nDays: int) -> [Dataframe]:
	series = []

	date = endDate
	if isinstance(endDate, str):
		date = datetime.date.fromisoformat(endDate)
	while nDays > 0:
		df = getDay(ticker, date.strftime('%Y-%m-%d'))
		if df is not None:
			series = [df] + series
			nDays -= 1
		date -= datetime.timedelta(days=1)

	return series

