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

def getComponentAt(rootComponent, p: Vector):
	# Find the deepest component that contains the click
	focus = rootComponent
	while len(focus.children) > 0:
		try:
			for c in focus.children:
				print(c, c.contains_point(p))
				if c.contains_point(p):
					focus = c
					raise StopIteration
		except StopIteration:
			continue
		break
	return focus

if __name__ == "__main__":
	rl.init_window(800, 600, 'rayplot')

	rl.set_target_fps(0)
	rl.set_window_state(rl.ConfigFlags.FLAG_WINDOW_RESIZABLE)
	rl.set_window_state(rl.ConfigFlags.FLAG_WINDOW_UNDECORATED)
	# rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)
	rl.enable_event_waiting()

	rootComponent = VBox(layout=Layout.TopAdjusted)
	rootComponent.add_child(Label('rayplot'))
	rootComponent.add_child(Ticker('AMD'))
	rootComponent.add_child(Ticker('^OMX'))
	rootComponent.add_child(Ticker('NVDA'))

	focus = rootComponent
	mouseDown = False
	while not rl.window_should_close():
		screenWidth = rl.get_screen_width()
		screenHeight = rl.get_screen_height()

		# Wait for events
		mousePos = Vector(rl.get_mouse_position().x, rl.get_mouse_position().y)
		if rl.is_mouse_button_pressed(0):
			mouseDown = True
			ev = MouseDownEvent(0, mousePos)

			focus = getComponentAt(rootComponent, mousePos)
			focus.event(ev)

		mouseMove = Vector(rl.get_mouse_delta().x, rl.get_mouse_delta().y)
		if mouseDown and (mouseMove.x != 0 or mouseMove.y != 0):
			ev = MouseMoveEvent(mouseMove)
			focus.event(ev)

		if rl.is_mouse_button_released(0):
			mouseDown = False
			ev = MouseUpEvent(0, mousePos)
			focus.event(ev)

		mouseWheel = rl.get_mouse_wheel_move_v().y
		if mouseWheel != 0:
			ev = MouseWheelEvent(mouseWheel)
			scrolled = getComponentAt(rootComponent, mousePos)
			if scrolled is not None:
				scrolled.event(ev)

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

