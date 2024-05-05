import argparse
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

import fetcher
from common import formatHourTime

class Predictor:
	def __init__(self, dumbStrat='random'):
		self.predictRanges = [datetime.timedelta(minutes=15)]  # Which time predictions this predictor will make
		self.predictWindow = 1  # How many days of history this predictor requires to make its prediction
		self.dumbStrat = dumbStrat

	def predict(self, hour: float, data: [fetcher.Dataframe]):
		# print('Predicting for {}T{}'.format(data[-1].date, formatHourTime(data[-1].openHour + hour)))
		if self.dumbStrat == 'random':
			return random.uniform(-1, 1)

		return 0

class LinRegPred(Predictor):
	def __init__(self):
		self.predictRanges = [datetime.timedelta(hours=1)]  # Which time predictions this predictor will make
		self.predictWindow = 1  # How many days of history this predictor requires to make its prediction

	def predict(self, hour: float, data: [fetcher.Dataframe]):
		# Formattera det som en kontinuerlig array, x skalan uttrycks i dagar
		y = []
		x = []
		# Add data for days up to the last one
		for day in range(len(data) - 1):
			y += [tick for tick in data[day].ticks]
			x += [day + i / len(data[day].ticks) for i in range(len(data[day].ticks))]

		# The last day might not have all the data available yet so only add what we have
		y += [tick for tick in data[-1].ticks[:int(hour * 60)]]
		hoursPerDay = data[-2].openTime if len(data) > 1 else 6.5
		x += [len(data) - 1 + i / 60 / hoursPerDay for i in range(len(data[-1].ticks[:int(hour * 60)]))]

		# # Cut off to only the last hour of data
		# y = y[-120:]
		# x = x[-120:]

		# print([a for a in zip(x, y)])
		reg = np.polyfit(x, y, 1)
		p = np.poly1d(reg)
		prediction = reg[0] * (x[-1] + self.predictRanges[0].seconds / 60**2 / hoursPerDay) + reg[1]

		# plt.plot(x, y)
		# plt.xlabel('x-axis')
		# plt.ylabel('y-axis')
		# plt.title('Plot of x vs y')
		# plt.plot(x, p(x), "r--")
		# plt.show()

		return prediction / y[-1] * 100 - 100

predictors: {str: Predictor} = dict({
	'random': Predictor('random'),
	'null': Predictor('null'),
	'linreg': LinRegPred()
})

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("algorithm", type=str, help="prediction algorithm. One of: {}".format(', '.join(predictors.keys())))
	parser.add_argument("-n", type=int, help="Number of runs", default=1)
	parser.add_argument("--history-depth", help="How many days back worth of history to train on", default=15)
	# parser.add_argument("--tickers", help="Which tickers to sample", default="AMD,NVDA,META,TSLA,^OMX")
	ticker = 'AMD'
	args = parser.parse_args()
	print(args)

	pred = predictors[args.algorithm]
	today = datetime.date.today()
	historyFrontBuffer = int(max([rnge.days for rnge in pred.predictRanges]) + 1)
	series = fetcher.getDataSeriesUpTo(ticker, today, pred.predictWindow + args.history_depth + historyFrontBuffer)
	errors = []
	for i in range(args.n):
		# Perform a single run
		sampleDaysBack = random.randint(0, args.history_depth)  # Sample a date
		sampleHour = random.uniform(pred.predictRanges[0].seconds / 60**2, series[-historyFrontBuffer - sampleDaysBack].openTime - pred.predictRanges[0].seconds / 60**2)  # Sample an hour on the day
		predictData = series[-historyFrontBuffer - sampleDaysBack - pred.predictWindow:-historyFrontBuffer - sampleDaysBack]

		prediction = pred.predict(sampleHour, predictData)
		closePrice = series[-historyFrontBuffer - sampleDaysBack].ticks[int(sampleHour * 60)]
		futurePrice = series[-historyFrontBuffer - sampleDaysBack].ticks[int(sampleHour * 60 + pred.predictRanges[0].seconds // 60)]
		correctDevelopment = futurePrice / closePrice * 100 - 100
		print('[{}]: Correct value={}, prediction={}'.format(predictData[-1].date, correctDevelopment, prediction))
		errors.append(abs(prediction - correctDevelopment) ** 2)

	mse = sum(errors) / len(errors)
	print('MSE: {}'.format(mse))

"""
Benchmarks:
	Only testing AMD to start with. Have made two dummy algorithms that any mildly competent algorithm should beat.

	`random`: Selects a random prediction between -1% to 1%. Scores an MSE of 0.5 for a prediction interval of 15m. Seems reasonable, if AMD hovers around 0% then the error should average around 0.5. If AMD moves randomly in the -1% to 1% interval we would expect an average error of 2/3. MSE of 0.5 is somewhere between those.

	`null`: Always responds 0%. This scores 0.2 on average, suggesting that AMD has an average volatility of 0.44%.

	Given the above tests we can say that any reasonable algorithm should be able to beat 0.2 MSE. The first sensible algorithm to test is linear regression over recent data.

	`linreg`: Makes a regression over recent data and predicts future movement by tracing the line. Depends on a hyperparameter for history depth. Different values should be tested.
		predict 15m given the last 15m: 0.97
		predict 15m given the last 30m: 0.61
		predict 15m given the last 1h: 0.60
		predict 15m given the last 2h: 0.82
		predict 1h given the last day: 0.82
"""

