# -*- encoding: utf-8 -*-
import os
from wx import *

Application = App(False)

Colors = {
	"Enter"		:"#393939", 
	"Click"		:"#242424", 
	"Default"	:"#444444",
	"Panel"		:"#555555"
	}

APPDIR = os.path.dirname(os.path.abspath(__file__))+"/"

execfile(APPDIR+"funcs.py")
execfile(APPDIR+"classes.py")
execfile(APPDIR+"gui.py")
execfile(APPDIR+"events.py")

#Загрузка
Application.MainLoop()