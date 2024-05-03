#!/usr/bin/env python3

import pyray as rl

from collections import namedtuple

from common import *


colors = namedtuple('Colors', 'background text containers faint')
colors.background = (0, 0, 0, 255)
colors.containers = (127, 88, 0, 255)
colors.text = (255, 177, 0, 255)
colors.faint = (int(255 / 3), int(177 / 3), 0, 255)
colors.good = (89, 162, 255, 255)
colors.bad = (255, 0, 0, 255)
colors.white = (255, 255, 255, 255)
colors.gray = (127, 127, 127, 255)

if __name__ == "__main__":
	rl.init_window(800, 600, 'rayplot')

	rl.set_target_fps(0)
	rl.set_window_state(rl.ConfigFlags.FLAG_WINDOW_RESIZABLE)
	# rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)
	rl.enable_event_waiting()

	rootComponent = VBox(layout=Layout.TopAdjusted)
	rootComponent.add_child(Label('abcdefg'))
	rootComponent.add_child(Ticker('AMD'))
	rootComponent.add_child(Ticker('^OMX'))
	rootComponent.add_child(Ticker('NVDA'))

	while not rl.window_should_close():
		screenWidth = rl.get_screen_width()
		screenHeight = rl.get_screen_height()

		# Wait for events

		rl.begin_drawing()
		rl.clear_background(colors.background)

		# Draw background grid
		for x in range(0, screenWidth, 100):
			rl.draw_line(x, 0, x, screenHeight, colors.faint)
		for y in range(0, screenHeight, 100):
			rl.draw_line(0, y, screenWidth, y, colors.faint)

		rootComponent.render(0, 0, rl.get_screen_width(), rl.get_screen_height())
		rl.end_drawing()
	rl.close_window()

