#
#	ElfKit is an automatic UI generator and manager library
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

"""ElfKit is a Python library to manage smart user interface. By smart,
this library intents to easily generate quick and responsive user
interface from the application described by its semantics: data items
and actions."""


from elfkit.base import *
import elfkit.gtk as gtk


def default_ui():
	"""Get the default user interface."""
	return gtk.DRIVER


class Application(Entity, Context):
	"""An application identify a program to the current OS and provides
	common facilities to manage the different aspects of an application.
	It provides a link with a specific UI library.
	
	The name parameter of the constructor is used for identify the
	application to the OS or to generate resources name relative to
	the application (like configuration data)."""
	
	def __init__(self, name, version = "", copyright = "", contact = "",
	website = "", description = "", **args):
		Entity.__init__(self, label=name, **args)
		Context.__init__(self, name, **args)
		self.name = name
		self.version = version
		self.copyright = copyright
		self.contact = contact
		self.website = website
		self.description = description
		self.quit_action = default_ui().quit_action

	def make_window(self, pane = None):
		"""Build and return a window for the current UI system."""
		return default_ui().open(self, pane)
		
	def setup(self):
		"""Called to let the application to set up its UI before the
		main loop."""
		pass
		
	def cleanup(self):
		"""Function called to perform actions when a quit action is 
		required from the user. Default does nothing."""
		return True
	
	def run(self, pane = None):
		"""Run the main loop of the application. The behaviour of this
		function depends a lot on the underlying UI implementation).
		If a pane is given, it is displayed."""
		self.setup()
		if pane != None:
			w = self.make_window(pane)
			w.open()
		default_ui().run()
		self.cleanup()

