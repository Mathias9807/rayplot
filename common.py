class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, b):
		if isinstance(b, (int, float)):
			return Vector(self.x + b, self.y + b)
		else:
			return Vector(self.x + b.x, self.y + b.y)

	def __sub__(self, b):
		if isinstance(b, (int, float)):
			return Vector(self.x - b, self.y - b)
		else:
			return Vector(self.x - b.x, self.y - b.y)

	def __mul__(self, b):
		if isinstance(b, (int, float)):
			return Vector(self.x * b, self.y * b)
		else:
			return Vector(self.x * b.x, self.y * b.y)

	def __floordiv__(self, b):
		if isinstance(b, (int, float)):
			return Vector(self.x / b, self.y / b)
		else:
			return Vector(self.x / b.x, self.y / b.y)

	def __truediv__(self, b):
		if isinstance(b, (int, float)):
			return Vector(self.x / b, self.y / b)
		else:
			return Vector(self.x / b.x, self.y / b.y)

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

def formatPercent(val: float, baseline: float):
	return '{}{}%'.format(' ' if val >= baseline else '', round(val / baseline * 100 - 100, 2))

def formatHourTime(val: float):
	return '{:02d}:{:02d}'.format(int(val), int((val - int(val)) * 60))

import pyray as rl

import main
from component import Component
from label import Label
from box import HBox, VBox, Layout, Spacer, XSpacer, YSpacer
from graph import Graph
from ticker import Ticker
