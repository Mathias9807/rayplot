from main import *


class Event:
	pass

class MouseDownEvent(Event):
	def __init__(self, button, p):
		self.button = button
		self.p = p

class MouseUpEvent(Event):
	def __init__(self, button, p):
		self.button = button
		self.p = p

class MouseMoveEvent(Event):
	def __init__(self, movement):
		self.movement = movement

class MouseWheelEvent(Event):
	def __init__(self, scroll):
		self.scroll = scroll

class Component:
	def __init__(self):
		self.parent = None
		self.children = []

		self.pos = Vector()
		self.bounds = Vector()

	def add_child(self, child):
		self.children.append(child)
		child.parent = self

	def min_width(self):
		return 0

	def max_width(self):
		return 1E9

	def min_height(self):
		return 0

	def max_height(self):
		return 1E9

	def contains_point(self, p):
		return p > self.pos and p - self.pos < self.bounds

	def event(self, event):
		if self.parent:
			self.parent.event(event)

	def render(self, x, y, w, h):
		self.pos = Vector(x, y)
		self.bounds = Vector(w, h)

