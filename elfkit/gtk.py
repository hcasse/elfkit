#
#	ElfKit upport for GtkUI.
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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import cairo

import elfkit.base as base
import elfkit.ui as ui

def error(msg):
	sys.stderr.write("ERROR: %s\n" % msg)


class MenuObserver:
	
	def __init__(self, item, action, con):
		self.item = item
		self.action = action
		self.con = con
	
	def on_update(self, var, val):
		self.item.set_sensitivie(self.action())

	def activate(self, item):
		self.action.apply(self.con)


def make_menu_action(action, menu, win):
	"""Build a menu for an action."""

	# create the item
	if action.icon != "":
		item = Gtk.ImageMenuItem(win.ui.get_icon(action.icon),
			label=action.label, always_show_image = True, use_stock = True)
	else:
		item = Gtk.MenuItem(action.label)
	if action.help != "":
		item.set_tooltip_text(action.help)
	menu.append(item)
	
	# connect the item
	obs = MenuObserver(item, action, win)
	for dep in action.get_deps():
		dep.add_observer(obs)
	item.connect("activate", obs.activate)


class CheckMenuObserver:

	def __init__(self, var, item):
		self.var = var
		self.item = item
		self.updating = False

	def on_toggled(self):
		if not self.updating:
			self.updating = True
			self.var.set(self.item.get_active())
			self.updating = False
	
	def on_update(self, var, val):
		if not self.updating:
			self.updating = True
			self.item.set_active(self.var.get())
			self.updating = False
	

def make_checked_menu(var, menu):
	"""Make a checked menu for a boolean variable."""
	
	# create the item
	item = Gtk.CheckMenuItem.new_with_label(var.label, active=var.get())
	menu.append(item)
	if var.help != "":
		item.set_tooltip_text(var.help)

	# connect it
	obs = CheckMenuObserver(var, item)
	var.add_observer(obs)
	item.connect("toggled", obs.on_toggle)


class EnumMenuObserver:
	
	def __init__(self, val, var, item):
		self.val = val
		self.var = var
		self.item = item
		self.updating = False
	
	def on_toggled(self, item):
		if not self.updating:
			self.updating = True
			if self.item.get_active():
				self.var.set(self.val.get_value())
			self.updating = False
	
	def on_update(self, var, val):
		if not self.updating and val == self.val.get_value():
			self.updating = True
			self.item.set_active(True)
			self.updating = False


def make_enum_menu(var, menu):
	group = []
	for val in var.type.get_values():
		
		# build the item
		item = Gtk.RadioMenuItem.new_with_label(group, val.label)
		group.append(item)
		menu.append(item)
		if val.get_value() == var.get():
			item.set_active(True)
		if var.help != "":
			if val.help != "":
				m = "%s %s" % (var.help, val.help)
			else:
				m = var.help
		elif val.help != "":
			m = val.help
		else:
			m = None
		if m != None:
			item.set_tooltip_text(m)
		
		# link the item
		obs = EnumMenuObserver(val, var, item)
		item.connect("toggled", obs.on_toggled)
		var.add_observer(obs)
		

def build_menu(menu, win):
	"""Build the given menu."""
	menubar = Gtk.MenuBar()
	for (name, items) in menu:
		top_item = Gtk.MenuItem(name)
		menubar.append(top_item)
		top_menu = Gtk.Menu()
		top_item.set_submenu(top_menu)
		for item in items:
			if isinstance(item, base.AbstractAction):
				make_menu_action(item, top_menu, win)
				continue
			elif isinstance(item, base.AbstractVar):
				if item.type.is_enum():
					make_enum_menu(item, top_menu)
					continue
				elif item.type.is_standard(bool):
					make_checked_menu(item, top_menu)
					continue
			error("don't known how to make a menu item with %s" % item)	
	return menubar


class RangeEntryObserver:
	
	def __init__(self, var):
		self.var = var
	
	def on_change_value(self, range, scrol, value):
		self.var.set(int(value))
		

def build_range_entry(var, win):
	"""Build a range entry."""
	entry = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL,
		Gtk.Adjustment(var.get(), var.type.low, var.type.up))
	entry.set_value(var.get())
	entry.set_digits(0)
	entry.set_hexpand(True)
	obs = RangeEntryObserver(var)
	entry.connect("change-value", obs.on_change_value)
	return entry


class EnumEntryObserver:
	
	def __init__(self, var):
		self.var = var
	
	def on_changed(self, cbox):
		self.var.set(self.var.type.get_values()[cbox.get_active()].get_value())
	

def build_enum_entry(var, win):
	"""Builf an enumerated entry."""
	store = Gtk.ListStore(str)
	i = 0
	for val in var.type.get_values():
		if val.get_value() == var.get():
			i = len(store)
		store.append([val.label])
	entry = Gtk.ComboBox.new_with_model(store)
	renderer = Gtk.CellRendererText()
	entry.pack_start(renderer, True)
	entry.add_attribute(renderer, "text", 0)
	entry.set_active(i)
	obs = EnumEntryObserver(var)
	entry.connect("changed", obs.on_changed)
	return entry


def build_entry(var, win):
	"""Build an entry to be embedded in a form."""
	if var.type.is_range():
		entry = build_range_entry(var, win)
	elif var.type.is_enum():
		entry = build_enum_entry(var, win)
	else:
		entry = Gtk.Label(var.label)
	if var.help != "":
		entry.set_tooltip_text(var.help)
	return entry

def build_form(vars, win):
	"""Build a form for the given variables."""
	grid = Gtk.Grid(column_spacing=8, row_spacing=8)
	i = 0
	for v in vars:
		label = Gtk.Label(v.label)
		label.set_xalign(1.)
		grid.attach(label, 0, i, 1, 1)
		item = build_entry(v, win)
		grid.attach_next_to(item, label, Gtk.PositionType.RIGHT, 1, 1)
		i = i + 1
	grid.show_all()
	return grid


class Window(ui.Window, base.Console):
	
	def __init__(self, u):
		ui.Window.__init__(self, u)
		self.ui = u
		self.win = None
		self.title = u.app.label
		self.menu = []

	def set_title(self, title):
		self.title = title
		if self.win != None:
			self.win.set_title(title)

	def set_menu(self, menu):
		self.menu = menu

	def init(self):

		# build the window
		self.win = Gtk.Window()
		self.win.connect("destroy", self.ui.quit)
		self.win.set_title(self.title)
		self.win.set_resizable(True)
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# build the menu
		if self.menu != None:
			menubar = build_menu(self.menu, self)
			box.pack_start(menubar, False, False, 0)

		# set the main content
		self.win.add(box)
		box.show_all()
		
	def open(self):
		if self.win == None:
			self.init()
		self.win.show_all()

	def close(self):
		self.win.hide()

	def info(self, msg):
		dialog = Gtk.MessageDialog(
				text=msg,
				message_type=Gtk.MessageType.INFO,
				buttons=Gtk.ButtonsType.CLOSE
			)
		dialog.run()
		dialog.hide()

	def warn(self, msg):
		dialog = Gtk.MessageDialog(
				text=msg,
				message_type=Gtk.MessageType.WARNING,
				buttons=Gtk.ButtonsType.CLOSE
			)
		dialog.run()
		dialog.hide()

	def error(self, msg):
		dialog = Gtk.MessageDialog(
				text=msg,
				message_type=Gtk.MessageType.ERROR,
				buttons=Gtk.ButtonsType.CLOSE
			)
		dialog.run()
		dialog.hide()

	def start_job(self, name, help="", icon=""):
		# TODO
		pass

	def end_job(self, name):
		# TODO
		pass
	
	def ask_yesno(self, question, deflt=False, help = "", icon=""):
		dialog = Gtk.MessageDialog(
				text=msg,
				message_type=Gtk.MessageType.QUESTION,
				buttons=Gtk.ButtonsType.YES_NO
			)
		res = dialog.run()
		dialog.hide()
		return res == Gtk.ResponseType.ACCEPT

	def ask_choice(self, question, list, deflt = None, help = "", icon=""):
		pass

	def ask_dialog(self, title="", vars=[], help=""):
		"""Open a dialog and ask the user to enter the given variables."""
		
		# save current values
		avars = []
		for v in vars:
			avars.append(v.copy())
		
		# manage the dialog
		form = build_form(avars, self)
		dialog = Gtk.Dialog(
			title,
			self.win,
			Gtk.DialogFlags.MODAL,
			buttons = [Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL])
		dialog.get_content_area().pack_start(form, True, True, 0)
		res = dialog.run()
		dialog.hide()
		
		# if cancelled, reset the variables
		if res != Gtk.ResponseType.OK:
			return False
		else:
			for i in range(0, len(vars)):
				vars[i].set(avars[i].get())
			return True


class UI(ui.UI):
	
	def __init__(self, app):
		ui.UI.__init__(self, app)
		self.quit_action = \
			base.Action(self.quit, label="Quit", icon=ui.QUIT_ICON, help="Leave the application.")
		self.icons = {
			ui.QUIT_ICON: Gtk.STOCK_QUIT
		}

	def make_window(self, **args):
		return Window(self, **args)
	
	def run(self):
		Gtk.main()

	def quit(self, con):
		if self.app.cleanup():
			Gtk.main_quit()

	def get_icon(self, name):
		try:
			return self.icons[name]
		except KeyError:
			return None

	def get_console(self):
		return self

		
