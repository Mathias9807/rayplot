from common import *
from fetcher import getDay
import datetime

class Ticker(Component):
	def __init__(self, ticker: str):
		super().__init__()
		self.ticker = ticker

		df = getDay(ticker, datetime.date.today().strftime('%Y-%m-%d'))
		# df = getDay(ticker, '2024-05-02')
		if df is None:
			return

		vbox = VBox()
		hbox = HBox(layout=Layout.LeftAdjusted)
		hbox.children.append(Label(ticker))
		hbox.children.append(Label(formatPercent(df.ticks[-1], df.openPr),
								  color=main.colors.good if df.ticks[-1] > df.openPr else main.colors.bad))
		hbox.children.append(XSpacer())
		hbox.children.append(Label(df.date))
		vbox.children.append(hbox)

		vbox.children.append(Graph(df))
		self.children.append(vbox)

	def min_width(self):
		return self.children[0].min_width() if len(self.children) > 0 else 0

	def min_height(self):
		return self.children[0].min_height() if len(self.children) > 0 else 0

	def max_width(self):
		return self.children[0].max_width() if len(self.children) > 0 else 0

	def max_height(self):
		return self.children[0].max_height() if len(self.children) > 0 else 0

	def render(self, x, y, w, h):
		if len(self.children) > 0:
			self.children[0].render(x, y, w, h)
