import main
from common import *
import pyray as rl

class Label(Component):
	def __init__(self, text: str, color=main.colors.text):
		self.text = text
		self.color = color
		self.padding = 20
		self.size = 24

	def min_width(self):
		# for some reason doesn't include final character so we just add one extra to compensate
		return rl.measure_text_ex(rl.get_font_default(), self.text + 'a', self.size, 0).x + self.padding

	def min_height(self):
		return rl.measure_text_ex(rl.get_font_default(), self.text + 'a', self.size, 0).y + self.padding

	def max_width(self):
		return self.min_width()

	def max_height(self):
		return self.min_height()

	def render(self, x, y, w, h):
		textSize = Vector(self.min_width(), self.min_height())
		tl = Vector(x, y)
		size = Vector(w, h)

		centeredTL = tl + size / 2 - textSize / 2

		# rl.draw_rectangle_lines(int(centeredTL.x), int(centeredTL.y), int(textSize.x), int(textSize.y), main.colors.text)
		rl.draw_text(self.text, int(centeredTL.x + self.padding/2), int(centeredTL.y + self.padding/2), self.size, self.color)
