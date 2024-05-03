from common import *
from math import log10, floor, ceil
from fetcher import Dataframe

class Graph(Component):
	def __init__(self, df: Dataframe):
		self.df = df
		self.startDate = df.date
		self.timeStart = 8 - df.openTime
		self.timeScope = 8

	def render(self, x, y, w, h):
		df = self.df

		drawArea = Vector(w - 4, h - 4)
		rl.draw_rectangle(int(x + 2), int(y + 2), int(w - 4), int(h - 4), main.colors.background)
		rl.draw_rectangle_lines(int(x + 2), int(y + 2), int(w - 4), int(h - 4), main.colors.text)

		maxPr = max([df.openPr] + df.ticks)
		minPr = min([df.openPr] + df.ticks)
		prMargin = (maxPr - minPr) * 0.05
		prRange = (maxPr + prMargin, minPr - prMargin)

		rl.draw_text(formatPercent(maxPr, df.openPr), int(x + 4), int(y + 4), 20, main.colors.text)
		rl.draw_text(formatPercent(minPr, df.openPr), int(x + 4), int(y + 2 + drawArea.y - 2 - 20), 20, main.colors.text)

		# Draw horizontal lines for different price levels
		prDiff = maxPr - minPr
		stepSize = 10 ** floor(log10(prDiff) - 1)
		targetNLines = int(h / 120)
		while prDiff / stepSize > targetNLines:
			stepSize *= 2
		while prDiff / stepSize < targetNLines:
			stepSize /= 2

		price = ceil(minPr / stepSize) * stepSize
		while price < maxPr:
			prY = (price - prRange[1]) / (prRange[0] - prRange[1])
			rl.draw_line(int(x + 2), int(y + 2 + drawArea.y - prY * drawArea.y), int(x + 2 + drawArea.x), int(y + 2 + drawArea.y - prY * drawArea.y), main.colors.faint)
			rl.draw_text(str(price), int(x + 10), int(y + 6 + drawArea.y - prY * drawArea.y), 20, main.colors.faint)

			price += stepSize

		ticks = [df.openPr] + df.ticks
		for i in range(len(ticks) - 1):
			prevTick = (ticks[i] - prRange[1]) / (prRange[0] - prRange[1])
			nextTick = (ticks[i + 1] - prRange[1]) / (prRange[0] - prRange[1])
			rl.draw_line(int(x + 2 + i / len(ticks) * drawArea.x), int(y + 2 + drawArea.y - prevTick * drawArea.y), int(x + 2 + (i+1) / len(ticks) * drawArea.x), int(y + 2 + drawArea.y - nextTick * drawArea.y), main.colors.text)

		# Draw vertical lines for dates and hours
		# firstDay = 

		def pToG(price):
			return (price - prRange[1]) / (prRange[0] - prRange[1])

		# Draw trend line
		xTicks = [t / len(ticks) for t in range(len(ticks))]
		xMid = sum(xTicks) / len(xTicks)
		yMid = sum(ticks) / len(ticks)
		b = sum([(ticks[i] - yMid) * (xTicks[i] - xMid) for i in range(len(ticks))]) / sum([(x - xMid) ** 2 for x in xTicks])
		a = sum(ticks) / len(ticks) - b * sum(xTicks) / len(xTicks)
		score = (sum([(a + i / len(xTicks) * b - ticks[i])**2 for i in range(len(ticks))])) / len(ticks)
		rl.draw_text(str(a + 0.5 * b), int(x + 10), int(y + 40), 20, main.colors.gray)
		rl.draw_text(str(b), int(x + 10), int(y + 70), 20, main.colors.gray)
		rl.draw_text(str(score), int(x + 10), int(y + 100), 20, main.colors.gray)
		rl.draw_line(int(x + 2), int(y + 2 + drawArea.y - pToG(a + 0.0 * b) * drawArea.y), int(x + 2 + drawArea.x), int(y + 2 + drawArea.y - pToG(a + 1.0 * b) * drawArea.y), main.colors.gray)

