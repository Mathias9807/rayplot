import datetime
import numpy as np

from fetcher import Dataframe, getDataSeriesUpTo


# Vill kunna kolla för en given ticker om deras senaste utveckling har följt en linjär kurva. Det skulle kunna indikera ett köpläge om någon viss aktie har haft en stabil tillväxt under en längre tid.

# Måste kunna göra regressioner på olika tidsskalor, senaste dagen, veckan eller månaden t.ex. Den beräknade regressionen kommer sedan bedömmas utifrån hur brant utvecklingen är, hur länge den har hållt upp och hur låg error regressionen gav.

# Skriv en funktion som tar en ticker och beräknar en regression med datan för de senaste n dagarna och returnerar kurvparametrarna och errorn.

def linearReg(ticker, nDays):
	# Hämta datan för perioden
	series = getDataSeriesUpTo(ticker, datetime.date.today(), nDays)

	# Formattera det som en kontinuerlig array, x skalan uttrycks i dagar
	y = [item for df in series for item in df.ticks]
	x = [day + i / len(series[day].ticks) for day in range(len(series)) for i in range(len(series[day].ticks))]
	# print([a for a in zip(x, y)])
	return np.polyfit(x, y, 1)

print(linearReg('NVDA', 2))

