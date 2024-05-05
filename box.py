from common import *
from enum import Enum

class Layout(Enum):
	Centered = 1
	LeftAdjusted = 2
	RightAdjusted = 3
	TopAdjusted = 2
	BottomAdjusted = 3

class HBox(Component):
	def __init__(self, layout = Layout.Centered):
		super().__init__()
		self.layout = layout
		self.children = []

	def min_width(self):
		return sum([c.min_width() for c in self.children])

	def min_height(self):
		return max([c.min_height() for c in self.children])

	def max_width(self):
		return sum([c.max_width() for c in self.children])

	def max_height(self):
		return max([c.max_height() for c in self.children])

	def render(self, x, y, w, h):
		super().render(x, y, w, h)
		rl.draw_rectangle_lines(int(x), int(y), int(w), int(h), main.colors.containers)

		height = min(max([c.max_height() for c in self.children]), h)

		# Given our width, how much can we give to each child
		widths = [c.min_width() for c in self.children]
		remaining = w - sum(widths)
		addedToSomeone = True
		while remaining > 0 and addedToSomeone:
			nextIncr = remaining / len(widths)
			addedToSomeone = False
			for i in range(len(widths)):
				# Increment each childs width with an n:th of the remaining space
				incr = min(nextIncr, self.children[i].max_width() - widths[i])
				widths[i] += incr
				remaining -= incr
				if incr > 0.001:
					addedToSomeone = True

		# print(widths)

		startX = 0
		totalWidth = sum(widths)
		if self.layout == Layout.RightAdjusted:
			startX = w - totalWidth
		if self.layout == Layout.Centered:
			startX = w / 2 - totalWidth / 2
		for i in range(len(self.children)):
			# print(startX + sum(widths[:i]), y, widths[i], height)
			self.children[i].render(x + startX + sum(widths[:i]), y, widths[i], height)

class VBox(Component):
	def __init__(self, layout=Layout.Centered):
		super().__init__()
		self.layout = layout
		self.children = []

	def min_width(self):
		if len(self.children) > 0:
			return max([c.min_width() for c in self.children])
		return 0

	def min_height(self):
		if len(self.children) > 0:
			return sum([c.min_height() for c in self.children])
		return 0

	def max_width(self):
		return max([c.max_width() for c in self.children])

	def max_height(self):
		return sum([c.max_height() for c in self.children])

	def render(self, x, y, w, h):
		super().render(x, y, w, h)
		rl.draw_rectangle_lines(int(x), int(y), int(w), int(h), main.colors.containers)

		if len(self.children) == 0:
			return

		width = min(max([c.max_width() for c in self.children]), w)

		# Given our height, how much can we give to each child
		heights = [c.min_height() for c in self.children]
		remaining = h - sum(heights)
		addedToSomeone = True
		while remaining > 0 and addedToSomeone:
			nextIncr = remaining / len(heights)
			addedToSomeone = False
			for i in range(len(heights)):
				# Increment each childs width with an n:th of the remaining space
				incr = min(nextIncr, self.children[i].max_height() - heights[i])
				heights[i] += incr
				remaining -= incr
				if incr > 0.001:
					addedToSomeone = True

		startY = 0
		totalHeight = sum(heights)
		if self.layout == Layout.BottomAdjusted:
			startY = h - totalHeight
		if self.layout == Layout.Centered:
			startY = h / 2 - totalHeight / 2
		for i in range(len(self.children)):
			self.children[i].render(x, y + startY + sum(heights[:i]), width, heights[i])

class Spacer(Component):
	pass

class XSpacer(Component):
	def max_height(self):
		return 0

class YSpacer(Component):
	def max_width(self):
		return 0

