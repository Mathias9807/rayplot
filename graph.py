from common import *
from math import log10, floor, ceil
from fetcher import Dataframe

class Graph(Component):
	def __init__(self, df: Dataframe):
		self.df = df
		self.startDate = df.date
		self.timeScope = 8
		self.timeStart = df.openTime - self.timeScope

		# Target the average price level in this scope, scaled to make every point visible
		visibleTicks = self.df.ticks[max(int(60 * self.timeStart), 0):int(60 * self.timeStart + 60 * self.timeScope)]
		self.yScope = (max(visibleTicks) - min(visibleTicks)) / 2 * 1.1
		self.yPos = (max(visibleTicks) + min(visibleTicks)) / 2
		print('yPos: {}, yScope: {}, max: {}, min: {}'.format(self.yPos, self.yScope, max(visibleTicks), min(visibleTicks)))

	def render(self, x, y, w, h):
		df = self.df

		drawTL = Vector(int(x + 2), int(y + 2))
		drawArea = Vector(w - 4, h - 4)
		rl.draw_rectangle(int(x + 2), int(y + 2), int(w - 4), int(h - 4), main.colors.background)
		rl.draw_rectangle_lines(int(x + 2), int(y + 2), int(w - 4), int(h - 4), main.colors.text)

		# Draw this day, from timeStart and with timeScope width
		# prData = [df.openPr] + df.ticks
		prData = df.ticks

		maxPr = -1E9
		minPr = 1E9

		def pToG(price):
			# print('price: {}, {} {} {}'.format(price, price - self.yPos, (price - self.yPos) / self.yScope, (price - self.yPos) / self.yScope * drawArea.y / 2 + drawArea.y / 2), flush=True)
			return (price - self.yPos) / self.yScope / 2 + 0.5

		# Draw a single day's worth of ticks on the graph
		maxPr = -1E9
		minPr = 1E9
		for i in range(len(prData) - 1):
			tx = i / 60 - self.timeStart  # Time in hours for this tick on screen
			if tx < 0:
				continue
			if tx > self.timeScope:
				break

			maxPr = max(maxPr, prData[i])
			minPr = min(minPr, prData[i])
			xCur = (tx + 1/60) / self.timeScope * drawArea.x
			xPrev = tx / self.timeScope * drawArea.x

			prevTick = pToG(prData[i])
			curTick = pToG(prData[i + 1])
			if prevTick < 0 or curTick < 0 or prevTick > 1 or curTick > 1:
				# print(self.yPos, self.yScope)
				# print(curTick, maxPr, tx, i, prData[i])
				continue
			rl.draw_line(int(drawTL.x + xPrev), int(drawTL.y + drawArea.y - prevTick * drawArea.y), int(drawTL.x + xCur), int(drawTL.y + drawArea.y - curTick * drawArea.y), main.colors.text)

		# Draw max and min percentages
		rl.draw_text(formatPercent(maxPr, df.openPr), drawTL.x, int(y + 4), 20, main.colors.text)
		rl.draw_text(formatPercent(minPr, df.openPr), drawTL.x, int(y + 2 + drawArea.y - 2 - 20), 20, main.colors.text)

		# Draw vertical lines for dates and hours
		if drawArea.x / self.timeScope > 100:
			hour = ceil(self.timeStart + df.openHour)
			while hour <= int(self.timeStart + df.openHour + self.timeScope):
				xPos = int((hour - self.timeStart - df.openHour) / self.timeScope * drawArea.x)
				if xPos < 50:
					hour += 1
					continue
				txt = formatHourTime(hour)
				rl.draw_text(str(txt), int(drawTL.x + 2 + xPos), int(drawTL.y + drawArea.y - 25), 20, main.colors.faint)
				rl.draw_line(drawTL.x + xPos, drawTL.y, drawTL.x + xPos, drawTL.y + int(drawArea.y), main.colors.faint)
				hour += 1

		# Draw horizontal lines for different price levels
		prDiff = self.yScope * 2
		stepSize = 10 ** floor(log10(prDiff))
		if stepSize / self.yScope * drawArea.y/2 > 100:
			stepSize /= 2

		price = ceil(minPr / stepSize) * stepSize
		while price < maxPr:
			prY = pToG(price)
			txt = str(price)
			if price.is_integer():
				txt = str(round(price))
			rl.draw_line(int(x + 2), int(y + 2 + drawArea.y - prY * drawArea.y), int(x + 2 + drawArea.x), int(y + 2 + drawArea.y - prY * drawArea.y), main.colors.faint)
			rl.draw_text(str(txt), int(x + 10), int(y + 6 + drawArea.y - prY * drawArea.y), 20, main.colors.faint)

			price += stepSize

		# # Draw trend line
		# xTicks = [t / len(ticks) for t in range(len(ticks))]
		# xMid = sum(xTicks) / len(xTicks)
		# yMid = sum(ticks) / len(ticks)
		# b = sum([(ticks[i] - yMid) * (xTicks[i] - xMid) for i in range(len(ticks))]) / sum([(x - xMid) ** 2 for x in xTicks])
		# a = sum(ticks) / len(ticks) - b * sum(xTicks) / len(xTicks)
		# score = (sum([(a + i / len(xTicks) * b - ticks[i])**2 for i in range(len(ticks))])) / len(ticks)
		# rl.draw_text(str(a + 0.5 * b), int(x + 10), int(y + 40), 20, main.colors.gray)
		# rl.draw_text(str(b), int(x + 10), int(y + 70), 20, main.colors.gray)
		# rl.draw_text(str(score), int(x + 10), int(y + 100), 20, main.colors.gray)
		# rl.draw_line(int(x + 2), int(y + 2 + drawArea.y - pToG(a + 0.0 * b) * drawArea.y), int(x + 2 + drawArea.x), int(y + 2 + drawArea.y - pToG(a + 1.0 * b) * drawArea.y), main.colors.gray)

