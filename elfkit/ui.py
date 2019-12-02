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

QUIT_ICON = 0

class Window:
	"""Abstract window implementation."""
	
	def __init__(self, ui):
		self.ui = ui
	
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


class UI:
	"""Class providing interface with the actual UI.
	UI provides also quit_action for quitting the application."""
	
	def __init__(self, app):
		self.app = app
		self.quit_action = None
	
	def make_window(self, **args):
		"""Build a window in the current UI."""
		pass
	
	def run(self):
		"""Run the UI."""
		pass
	
	def quit(self):
		"""Quit the application."""
		pass
		
	def get_console(self):
		"""Get the console used in this window."""
		return None

