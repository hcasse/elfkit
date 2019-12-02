#
#	Base classes of ElfKit.
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

import sys

NO_TYPE = 0
STANDARD = 1
ENUM = 2
RANGE = 3


class Console:
	"""A console is in charge of implementing dialog with the human user
	in the better way according to the current UI."""
	
	def info(self, msg):
		"""Display the given message as an information."""
		sys.stderr.write("%s\n" % msg)

	def warn(self, msg):
		"""Display the given message as a warning."""
		sys.stderr.write("WARNING: %s\n" % msg)

	def error(self, msg):
		"""Display the given message as an error."""
		sys.stderr.write("ERROR: %s\n" % msg)

	def start_job(self, name, help="", icon=""):
		"""Start a job: all messages will be grouped and displayed
		in a grouped way to the user, under the label name."""
		sys.stderr.write("STARTING: %s\n" % name)
	
	def end_job(self, name):
		"""Called to end the current job."""
		sys.stderr.write("ENDED:\n")
	
	def ask_yesno(self, question, deflt=False, help = "", icon=""):
		"""Ask a question to the user with answer YES or NO.
		Return True for yes, False for no."""
		while True:
			sys.stdout.write("%s [%s|%s]: " % (
				question,
				"YES" if deflt == True else "yes",
				"NO" if deflt == False else "no"))
			sys.stdout.flush()
			a = sys.stdin.read()
			if a == "" or a == "\n":
				return delft
			if a[-1] == "\n":
				a[:-1]
			a = a.capitalize()
			if a == "YES":
				return True
			elif a == "NO":
				return False
			elif a == "HELP":
				sys.stdout.write("%s\n" % help)
			else:
				sys.stdout.write("Please enswer by YES or NO.\n")
			
	def ask_choice(self, question, list, deflt = None, help = "", icon=""):
		"""Ask the user to select an item from the given list.
		Return the selected item or None if the question has been cancelled."""
		sys.stdout.write("%s\n" % question)
		for i in range(0, len(list)):
			sys.stdout.write("%d. %s\n" % (i+1, list[i]))
		while True:
			sys.stdout.write("Your choice [1-%d%d]: " % (
				len(list),
				", default=%d" % list.index(deflt) if deflt != None else ""))
			sys.stdout.flush()
			a = sys.stdin.read()
			if a == "" or a == "\n":
				if deflt != None:
					return deflt
				else:
					sys.stdout.write("Please, perform a choice.\n")
			else:
				if a[-1] == "\n":
					a = a[:-1]
				try:
					n = int(a)
					if n < 1 or n > len(list):
						sys.stdout.write("Please, write a number in [1, %d].\n" % len(list))
					else:
						return list[n - 1]
				except ValueError:
					if a.capitalize() == "HELP":
						sys.stdout.write("%s\n" % help)
					else:
						sys.stdout.write("Please, write a number.")

TEXT_CONSOLE = Console()
	

class Subject:
	"""This is the base of objects supporting observations.
	It provides all facilities to register/unregister observers and to
	propgate change events."""
	
	def __init__(self):
		self.obss = []
		
	def add_observer(self, obs):
		"""Add an observer."""
		self.obss.append(obs)
		
	def remove_observer(self, obs):
		"""Remove an observer."""
		self.obss.remove(obs)
	
	def trigger(self, type, fun):
		"""Trigger an event on all observers of the given type using the
		function fun that is called with the observer as parameter."""
		for obs in self.obss:
			if isinstance(obs, type):
				fun(obs)


class Entity(Subject):
	"""An entity represents an object in the UI that is make viewvable
	to a human user. It is composed of a label (that can be translated),
	an icon, an help message, etc. In the constructor, the group 
	corresponds to the logical group that owns this entity."""
	
	def __init__(self, label = "", icon = "", help = "", group = None):
		Subject.__init__(self)
		self.label = label
		self.icon = icon
		self.help = help
		self.group = group
	
	def get_label(self):
		"""Get the possibly translated label of the entity."""
		return self.label

	def get_icon(self, app):
		"""Get the icon of the label. The app is the current
		application."""
		return None
	
	def get_help(self):
		"""Get the helper message, possibly translated."""
		return self.help

	def copy(self, v = None):
		if v == None:
			v = Entity()
		v.label = self.label
		v.icon = self.icon
		v.help = self.help
		v.group = self.group
		return v


class Type(Entity):
	"""These objects describes the types of the values managed by the UI.
	Each type has a kind like ENUM (enumerated type) or STANDARD
	(Python standard type like int, float, str, bool)."""

	def __init__(self, kind, **args):
		Entity.__init__(self, **args)
		self.kind = kind
	
	def is_standard(self, type = None):
		"""Test if the type is a standard and if the parameter type is
		not none, test if it is equal."""
		return False
	
	def is_enum(self):
		"""Test if the type is enumerated."""
		return False
	
	def is_range(self):
		"""Test if the type is a range."""
		return False
	
	def get_default(self):
		"""Get the default value for the current type."""
		return None

DEFAULT_VALUES = {
	bool: False,
	int: 0,
	float: 0.,
	str: ""
}
class StandardType(Type):
	"""Type representing standard types of Python."""
	
	def __init__(self, type, **args):
		Type.__init__(STANDARD, **args)
		self.type = type

	def is_standard(self, t):
		return t == None or self.type == t

	def get_default(self):
		try:
			return DEFAULT_VALUES[self.type]
		except KeyError:
			return None


class EnumValue(Entity):
	"""A value for an enumerated type."""
	
	def __init__(self, value, **args):
		Entity.__init__(self, **args)
		self.value = value

	def get_value(self):
		return self.value


class EnumType(Type):
	"""An enumerated type."""
	
	def __init__(self, values, **args):
		Type.__init__(self, ENUM, **args)
		self.values = values
	
	def get_values(self):
		return self.values

	def is_enum(self):
		return True

	def get_default(self):
		return self.values[0]


class RangeType(Type):
	"""A type representing a sub-range of integers."""
	
	def __init__(self, low, up, **args):
		Type.__init__(self, RANGE, **args)
		self.low = low
		self.up = up

	def is_range(self):
		return True
	
	def get_default(self):
		return self.low


def get_default(self):
	return self.low


class EntityObserver:
	"""Base class to be implemented for an entity change observer."""
	
	def on_change(self, entity):
		"""Function called when the observed entity is changed."""
		pass


class Group(Entity):
	"""A group represents the aggregation of diffrerent resources
	facilities encompassing, but not limited to, tranlations, configuration.
	Common groupes includes application, plug-ins and libraris."""
	
	def __init__(self, name, **args):
		Entity.__init__(self, **args)
		self.name = name


class VarObserver:
	"""Base class to be implemented for a variable change observer."""
	
	def on_update(self, var, val):
		"""Function called when the observed variable is changed.
		var is the chanegd variable and val is the new value."""
		pass


class UpdateFun(VarObserver):
	"""A variable observer that simply call a function."""
	
	def __init__(self, fun):
		self.fun = fun

	def on_update(self, var, val):
		self.fun(var, val)


class AbstractVar(Entity):
	"""The AbstractVar class is used as an observable points for the widgets
	of the user interface to detect its changes and update themselves.
	This class is abstract and is usually employed as Var or AttrVar."""
	
	def __init__(self, type, **args):
		Entity.__init__(self, **args)
		Subject.__init__(self)
		self.type = type

	def trigger_update(self, val):
		self.trigger(VarObserver, lambda obs: obs.on_update(self, val))

	def copy(self, v = None):
		"""Build a variable as a copy the current variable."""
		if v == None:
			v = AbstractVar(self.type)
		else:
			v.type = self.type
		Entity.copy(self, v)
		return v

	def __add__(self, op):
		return self.get().__add__(op)
	
	def __sub__(self, op):
		return self.get().__sub_(op)


class Var(AbstractVar):
	"""Var class is the implmentation for a singla value of an AbstractVar.
	It provides an observable point for local or global variable of the
	program. It provides facilities to modify the variable and to
	signal the observer about the modifications."""
	
	def __init__(self, val, t = None, **args):
		if t == None:
			if isinstance(val, Type):
				t = val
				val = t.get_default()
			else:
				t = StandardType(type(val))
		AbstractVar.__init__(self, t, **args)
		self.val = val

	def get(self):
		return self.val
	
	def set(self, val):
		self.val = val
		self.trigger_update(self.get())
	
	def copy(self, v = None):
		if v == None:
			v = Var(self.val, self.type)
		else:
			v.val = self.Val
		AbstractVar.copy(self, v)
		return v


class AbstractAction(Entity, Subject):
	"""An action is used to identify the possible actions of a user and
	to trigger this action. In addition, it provides a check function to
	check if an action is available at a particular time.
	To to this, an action is at the same time a subject and an observer."""
	
	def __init__(self, deps = None, **args):
		Entity.__init__(self, **args)
		Subject.__init__(self)
		if deps == None:
			self.deps = []
		else:
			self.deps = deps
	
	def apply(self, con):
		"""Launch the action. con is a console that may be used to
		display human user output or to interact with him."""
		pass
	
	def check(self):
		"""Function called to know if the action is allowed.
		Return True if the action is allowed, False else."""
		pass

	def get_deps(self):
		"""Get the dependencies of the action."""
		return self.deps


def no_apply(con):
	"""Empty action."""
	pass


def no_check():
	"""Empty check. Always return True."""
	return True


class Action(AbstractAction):
	"""A simple action based on the call of 2 functions: afun when an
	application of the function is performed, cfun (optional) to check the
	action."""
	
	def __init__(self, afun, cfun = no_check, **args):
		AbstractAction.__init__(self, **args)
		self.afun = afun
		self.cfun = cfun
	
	def apply(self, con):
		self.afun(con)
	
	def check(self):
		return self.cfun()

