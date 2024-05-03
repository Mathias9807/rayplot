from main import *


class Component:
	def __init__(self):
		self.children = []

	def add_child(self, child):
		self.children.append(child)

	def min_width(self):
		return 0

	def max_width(self):
		return 1E9

	def min_height(self):
		return 0

	def max_height(self):
		return 1E9

	def event(self):
		pass

	def render(self, x, y, w, h):
		pass

