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

"""Views defines content organization to be displayed to the user.
More common pane includes SwitchView to select an action, FormView
to display a form, etc."""

from elfkit import base

class Observer:
	""""Observer for a view;"""

	def on_show(self, view):
		"""Called when a view is displayed."""
		pass

	def on_hide(self, view):
		"""Called when a view is hidden."""
		pass


class View(base.Entity):
	"""Parent class of all panes."""

	def __init__(self, **args):
		base.Entity.__init__(self, **args)

	def show(self):
		""""Called when the view is about to be displayed."""
		self.trigger(Observer, lambda obs: obs.on_show(self))

	def hide(self):
		""""Called when the view is no more displayed."""
		self.trigger(Observer, lambda obs: obs.on_hide(self))


class Switch(View):
	""""A switch pane takes a list of actions as parameter and ask the
	user to choose one."""

	def __init__(self, acts, **args):
		View.__init__(self, label = "Switch View", **args)
		self.acts = acts

	def get_actions(self):
		"""Get the actions of the switch."""
		return self.acts
