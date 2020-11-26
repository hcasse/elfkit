#!/usr/bin/python3

from elfkit import *
from elfkit import base
from elfkit import view

APP = Application("hello")

but1_act = base.Action(
	label = "Button 1",
	help = "Select button 1!",
	icon = ui.QUIT_ICON,
	afun = lambda ctx: print("Button1")
)
but2_act = base.Action(
	label = "Button 2",
	help = "Select button 2!",
	icon = ui.QUIT_ICON,
	afun = lambda ctx: print("Button2"),
	cfun = lambda: False
)
but3_act = base.Action(
	label = "Button 3",
	help = "Select button 3!",
	icon = ui.QUIT_ICON,
	afun = lambda ctx: print("Button3")
)

APP.run(view.Switch([but1_act, but2_act, but3_act]))
