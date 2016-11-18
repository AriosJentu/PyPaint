# -*- encoding: utf-8 -*-
IsDrawing = False
IsPanelMoving = False

CurrentPolygon = 3

Description = "Векторный графический редактор"

def OnFrameResize(evt):
	w, h = PaintFrame.GetSize()
	PaintSidePanel.SetSize(Size(115, h-51))

	w, h = w-114, h-51
	DrawScroller.SetSize(Size(w, h))

	x, y = DrawPanel.GetPosition()
	sw, sh = DrawPanel.GetSize()

	#print("RESIZING:", x, y, w, sw, w-sw, h, sh, h-sh)

	if x < w-sw:
		x = w-sw
	if y < h-sh:
		y = h-sh

	if x > 0:
		x = 0
	if y > 0:
		y = 0

	if w > sw:
		sw = w
	if h > sh:
		sh = h

	DrawPanel.Move(Point(x, y))
	#DrawPanel.SetSize(Size(sw, sh))
	#print(Paint.MinW, Paint.MinH, sw, sh)
	
	x, y = PaintParameters.GetPosition()
	PaintParameters.SetSize(Size(114, h-y))
	for but in PaintButtons:
		but.Property.Panel.SetSize(Size(114, h-y))


def OnPaint(evt):

	#Paint.Clear()
	Redraw()

SavingClickCoords = []
def OnPaintMouseDown(evt):

	global CurrentFigure, CurrentTool, IsDrawing, SavingClickCoords, IsPanelMoving, CurrentPolygon

	#print(CurrentTool.Name, CurrentTool.Name == "Move")

	if CurrentTool.IsDrawTool != False:

		IsDrawing = True
		#print(True)

		SavingClickCoords = [evt.GetPosition().x, evt.GetPosition().y]

		CurrentFigure = Figure()
		CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])
		if CurrentTool.Continious != True:
			CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])

		CurrentFigure.Tool = CurrentTool
		CurrentFigure.PenColor = CurrentColour[0]
		CurrentFigure.BrushColor = CurrentColour[1]
		CurrentFigure.BrushSize = CurrentToolSize*(CurrentZoom/100)
		CurrentFigure.Polygons = CurrentPolygon

		OnPaintMouseMove(evt)

	elif CurrentTool.Name == "Move":

		IsPanelMoving = True
		#print(IsDrawing)
		SavingClickCoords = [GetMousePosition().x, GetMousePosition().y, DrawPanel.GetPosition().x, DrawPanel.GetPosition().y]


def OnPaintMouseUp(evt):

	global CurrentFigure, CurrentTool, IsDrawing, DrawPanel, IsPanelMoving

	IsDrawing = False
	IsPanelMoving = False
	#print(IsDrawing, "ON UP")

	#print(evt.GetPosition().y, CurrentTool == Pen)
	if CurrentTool.IsDrawTool != None:

		CurrentFigure = None



def OnPaintMouseMove(evt):

	global IsDrawing, IsPanelMoving
	#print(IsPanelMoving)
	#print(CurrentColour[0], CurrentColour[1], CurrentToolSize, CurrentZoom)
	#print(DrawPanel.ScreenToClient(GetMousePosition()))
	#print(IsDrawing)
	if IsDrawing == True:

		global CurrentFigure, CurrentTool, SavingClickCoords
		#print(CurrentTool, Pen)

		if CurrentTool.Continious == True:
		
			CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])
		
		else:

			x, y = SavingClickCoords[0], SavingClickCoords[1]
			w, h = evt.GetPosition()

			CurrentFigure.Points[0] = [x, y]
			CurrentFigure.Points[1] = [w, h]

		Redraw(True)

	if IsPanelMoving == True:

		#Redraw()

		w, h = DrawScroller.GetSize()
		sw, sh = DrawPanel.GetSize()

		#print(w, h, sw, sh, w < sw or h < sh)
		#print(SavingClickCoords[2], SavingClickCoords[3])
		#print("\n")

		if w < sw or h < sh or SavingClickCoords[2] < 0 or SavingClickCoords[3] < 0 :

			curX, curY = GetMousePosition()
			difX, difY = curX-SavingClickCoords[0], curY-SavingClickCoords[1]
			#print(SavingClickCoords[0], SavingClickCoords[1], curX, curY)
			newX, newY = SavingClickCoords[2]+difX, SavingClickCoords[3]+difY
			#print(newX, newY, difX, difY)

			#print(newX, newY)

			if newX < w-sw: newX = w-sw
			if newY < h-sh: newY = h-sh

			if newX > 0: newX = 0
			if newY > 0: newY = 0

			#print(newX, newY, curX, curY, w, sw, h, sh)

			DrawPanel.Move(Point(newX, newY))

def OnPenPropertyBrushSize(evt):
	global ContLine, CurrentToolSize, DrawingToolsTable

	#print(ContLine.GUI["BS"].GetValue())
	CurrentToolSize = CurrentTool.GUI["BS"].GetValue()
	for i in DrawingToolsTable:
		i.GUI["BS"].SetValue(CurrentToolSize)

def Redraw(isCalcSizes = False):
	Paint = PaintZone(DrawPanel)
	Paint.Clear()

	Paint.BeginDrawing()
	for i in Figures:
		Paint.DrawFigure(i)

	if isCalcSizes == True:
		Paint.CalcSizes()

	Paint.EndDrawing()

def ChangePolygons(evt):
	global CurrentPolygon
	CurrentPolygon = int(Polygon.GUI["AN"].GetValue())

def AtStart(evt):
	global DrawPanel
	DrawPanel.Move(Point(0, 0))

def OnQuit(evt):

	dialog = MessageDialog(None, "Действительно желаете закрыть это приложение?", "Выход", YES_NO)

	if dialog.ShowModal() == ID_YES:
		exit()
	else:
		dialog.Destroy()

def Undo(evt):
	global Figures

	if len(Figures) > 0:
		del Figures[len(Figures)-1]
		Redraw(True)

def ClearPaint(evt):
	global Figures

	Figures = []
	Redraw(True)

def ShowAbout(evt):

	info = AboutDialogInfo()
	info.SetIcon(Icon(APPDIR+"icons/logo.png"))
	info.SetName("PyPaint")
	info.SetVersion("1.0")
	info.SetDescription(Description)
	info.SetCopyright("(C) 2016.11 Arios Jentu")
	info.SetWebSite("https://github.com/AriosJentu")
	info.AddDeveloper("Максимов Павел Александрович\n(AriosJentu) [Б8103-а]")

	AboutBox(info)

PaintFrame.Bind(EVT_SIZE, OnFrameResize)
PaintFrame.Bind(EVT_CLOSE, OnQuit)

FileMenu.Bind(EVT_MENU, OnQuit, id=ID_EXIT)
FileMenu.Bind(EVT_MENU, Undo, id=ID_UNDO)
FileMenu.Bind(EVT_MENU, Redraw, id=ID_REDRAW)
FileMenu.Bind(EVT_MENU, ClearPaint, id=ID_CLEAR)

HelpMenu.Bind(EVT_MENU, ShowAbout, id=ID_ABOUT)

DrawPanel.Bind(EVT_PAINT, OnPaint)
DrawPanel.Bind(EVT_LEFT_DOWN, OnPaintMouseDown)
DrawPanel.Bind(EVT_LEFT_UP, OnPaintMouseUp)
DrawPanel.Bind(EVT_MOTION, OnPaintMouseMove)

for i in DrawingToolsTable:
	i.GUI["BS"].Bind(EVT_SPINCTRL, OnPenPropertyBrushSize)

Polygon.GUI["AN"].Bind(EVT_SPINCTRL, ChangePolygons)
Move.GUI["ST"].Bind(EVT_LEFT_DOWN, AtStart)

def onDown(evt):
	print("DOWN")

def onUp(evt):
	print("UP")