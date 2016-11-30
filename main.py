# -*- encoding: utf-8 -*-
import os
from wx import *

Application = App(False)

Colors = {
	"Selection"	:"#D97272",
	"Enter"		:"#393939", 
	"Click"		:"#242424", 
	"Default"	:"#444444",
	"Panel"		:"#555555"
	}

CurrentTool = None
CurrentFigure = None
CurrentColour = ["#000000", "#FFFFFF"]
CurrentToolSize = 1
CurrentZoom = 100
CurrentPolygon = 3
CurrentRadius = 5
CurrentAngle = 0
CurrentBrushStyle = TRANSPARENT
CurrentPenStyle = SOLID

APPDIR = os.path.dirname(os.path.abspath(__file__))+"/"

execfile(APPDIR+"funcs.py")
execfile(APPDIR+"classes.py")
execfile(APPDIR+"gui.py")
execfile(APPDIR+"events.py")

#Загрузка
Application.MainLoop()