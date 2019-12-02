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

from elfkit.base import *
import elfkit.gtk as gtk

class Application(Group):
	"""An application identify a program to the current OS and provides
	common facilities to manage the different aspects of an application.
	It provides a link with a specific UI library.
	
	The name parameter of the constructor is used for identify the
	application to the OS or to generate resources name relative to
	the application (like configuration data)."""
	
	def __init__(self, name, version = "", copyright = "", contact = "",
	website = "", description = "", **args):
		Group.__init__(self, name, **args)
		self.name = name
		self.version = version
		self.copyright = copyright
		self.contact = contact
		self.website = website
		self.description = description
		self.ui = gtk.UI(self)
		self.quit_action = self.ui.quit_action

	def make_window(self):
		"""Build and return a window for the current UI system."""
		return self.ui.make_window()
		
	def setup(self):
		"""Called to let the application to set up its UI before the
		main loop."""
		pass
		
	def cleanup(self):
		"""Function called to perform actions when a quit action is 
		required from the user. Default does nothing."""
		return True
	
	def run(self):
		"""Run the main loop of the application. The behaviour of this
		function depends a lot on the underlying UI implementation)."""
		self.setup()
		self.ui.run()
		self.cleanup()
	
