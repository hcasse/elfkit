#
#	Abstract User Interface.
#	Copyright (C) 2019  Hugues Casse <hug.casse@gmail.com>
#
#	This file is part of ElfKit.
#
#	ElfKit is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	ElfKit is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with ElfKit.  If not, see <https://www.gnu.org/licenses/>.
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""The UI is the common interface hiding the detail of the actual
user interface."""

import elfkit.base

# default icons
QUIT_ICON = 0
ABOUT_ICON = 1
ADD_ICON = 2
APPLY_ICON = 3
CANCEL_ICON = 4
CLEAR_ICON = 5
CLOSE_ICON = 6

BOLD_ICON = 50

CDROM_ICON = 100

# icon size
MENU_ICON_SIZE = 0
SMALL_TOOLBAR_ICON_SIZE = 1
LARGE_TOOLBAR_ICON_SIZE = 2
BUTTON_ICON_SIZE = 3
DND_ICON_SIZE = 4
DIALOG_ICON_SIZE = 5


class Widget:
	"""A widge to be displayed."""
	pass


class DrawingArea:
	"""A class dedicated to paint on."""
	
	def get_rgb(self, r, g, b):
		"""Obtain a color with given RGB values. (r, g, b) may
		be floats beween [0., 1.] or integer bewteen [0, 255]."""
		return None
	
	def set_color(self, color):
		"""Set the current color."""
		pass
	
	def box(self, x, y, w, h):
		"""Draw an empty box at position (x, y) with width w and height h
		with the current color."""
		pass
	
	def fill_box(self, x, y, w, h):
		"""Draw a full box at position (x, y) with width w and heihgt h
		with the current color."""
		pass
	
	def draw_image(self, image, x, y):
		"""Draw the given image at the position (x, y):"""
		pass


class Painter:
	"""Class used by the Canvas to paint itself."""
	
	def paint(self, draw, x, y, w, h):
		"""Called to repaint the area (x, y)-(w, h) on the given draw
		port."""
		pass


class Canvas:
	"""A canvas is a UI interface letting the user to draw different shapes,
	images, text, etc."""	
	
	def set_size(self, w, h):
		"""Set the size in pixel of the image on the canvas."""
		pass


class Frame:
	"""Frame of a user interface."""
	
	def __init__(self, app, driver):
		self.driver = driver
		self.app = app

	def set_title(self, title):
		"""Set the title of the window."""
		pass
	
	def open(self):
		"""Open the window."""
		pass
	
	def close(self):
		"""Close the window."""
		pass
	
	def get_console(self):
		"""Get the console corresponding the window."""
		return base.TEXT_CONSOLE

	def ask_dialog(self, title="", vars=[], help=""):
		"""Open a dialog and ask the user to enter the given variables."""
		pass

	def make_image(self, path):
		"""Obtain an image from the given path."""
		return None
	
	def make_canvas(self, painter, **args):
		"""Build a canvas for the current window."""
		return None

	def set_content(self, widget):
		"""Set the content of the window."""
		pass

	def get_context(self, entity):
		"""Ge the context for the given entity. Usually, application
		entities does not record the application as context:
		this function does it."""
		c = entity.get_context()
		if c == None:
			entity.context = self.app
		return c

	def get_driver(self):
		"""Return the User Interface of the window."""
		return self.driver


class Driver:
	"""Class provdriving a human interface device. This device may
	be a screen, a HTTP server, a terminal or whatever let communicate
	with a human user."""
	
	def open(self, app, pane = None, **args):
		"""Build a frame in the current driver.
		If a pane is provided, it is the main content of the created
		window."""
		pass
	
	def run(self):
		"""Run the UI."""
		pass
	
	def get_console(self):
		"""Get the console used in this window."""
		return None

	def quit(self):
		"""Stop the execution of this UI."""
		pass

