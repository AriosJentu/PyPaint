# -*- coding: utf-8 -*-
IsDrawing = False
IsPanelMoving = False
IsLoop = False
IsSelector = False

Description = "Векторный графический редактор\nПроект распространяется свободно"

def OnFrameResize(evt):
	w, h = PaintFrame.GetSize()
	PaintSidePanel.SetSize(Size(115, h-51))

	w, h = w-114-3, h-51
	DrawScroller.SetSize(Size(w, h))

	x, y = DrawPanel.GetPosition()
	sw, sh = Paint.MinW, Paint.MinH

	if x < w-sw: x = w-sw
	if y < h-sh: y = h-sh

	if x > 0: x = 0
	if y > 0: y = 0

	if w > sw: sw = w
	if h > sh: sh = h

	DrawPanel.Move(Point(x, y))
	Redraw(True)

	x, y = PaintParameters.GetPosition()
	PaintParameters.SetSize(Size(114, h-y))
	for but in PaintButtons:
		but.Property.Panel.SetSize(Size(114, h-y))


def OnPaint(evt):

	Redraw()

SavingClickCoords = []
def OnPaintMouseDown(evt, MouseButton):

	global CurrentFigure, CurrentTool, IsDrawing, IsLoop, SavingClickCoords, IsPanelMoving, CurrentPolygon, Paint, IsSelector

	SavingClickCoords = [evt.GetPosition().x, evt.GetPosition().y, GetMousePosition().x, GetMousePosition().y]
	
	if CurrentTool.Name == "Move" or MouseButton == "middle":

		IsPanelMoving = True
		SavingClickCoords = [GetMousePosition().x, GetMousePosition().y, DrawScroller.GetViewStart().x, DrawScroller.GetViewStart().y]
		return False

	elif CurrentTool.Name == "Scale":

		IsLoop = True

	elif CurrentTool.Name == "Selection":

		IsSelector = True		


	elif CurrentTool.IsDrawTool != False:

		IsDrawing = True

		CurrentFigure = CurrentTool.Figure()
		CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])
		if CurrentTool.Continious != True:
			CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])

		CurrentFigure.Tool = CurrentTool
		CurrentFigure.PenColor = CurrentColour[0] if MouseButton == "left" else CurrentColour[1]
		CurrentFigure.BrushColor = CurrentColour[1] if MouseButton == "left" else CurrentColour[0]
		CurrentFigure.BrushSize = CurrentToolSize
		CurrentFigure.Polygons = CurrentPolygon
		CurrentFigure.PenStyle = CurrentPenStyle
		CurrentFigure.BrushStyle = CurrentBrushStyle
		CurrentFigure.Radius = CurrentRadius
		CurrentFigure.Angle = CurrentAngle

	OnPaintMouseMove(evt)


def OnPaintMouseUp(evt):

	global CurrentFigure, CurrentTool, IsDrawing, DrawPanel, IsPanelMoving, IsSelector

	IsDrawing = False
	IsPanelMoving = False
	IsSelector = False

	if CurrentTool.IsDrawTool != None:

		CurrentFigure = None

		Redraw(True)


ScalingArguments = []
def OnPaintMouseMove(evt):

	global IsDrawing, IsLoop, IsPanelMoving, DrawScroller, Paint, IsSelector

	if IsDrawing or IsLoop or IsSelector:

		global CurrentFigure, CurrentTool, SavingClickCoords, ScalingArguments

		if CurrentTool.Continious == True:
		
			CurrentFigure.Points.append([evt.GetPosition().x, evt.GetPosition().y])
		
		else:

			ax, ay = DrawPanel.GetPosition()

			x, y = SavingClickCoords[0], SavingClickCoords[1]
			w, h = evt.GetPosition().x, evt.GetPosition().y

			if CurrentFigure:
				CurrentFigure.Points[0] = [x, y]
				CurrentFigure.Points[1] = [w, h]

			if IsLoop or IsSelector:
				Redraw()
				
				Paint = PaintZone(DrawPanel)
				
				ScalingArguments = [x, y, w, h]

				Paint.BeginDrawing()
				
				Paint.SetBrush(Brush(Colors["Selection"], CROSSDIAG_HATCH if IsLoop else TRANSPARENT))
				Paint.SetPen(Pen(Colors["Selection"], 1 if IsLoop else 2, DOT if IsLoop else LONG_DASH))
				Paint.DrawRect(x, y, w, h)

				Paint.EndDrawing()

				if IsSelector:
					SelectFiguresInRange(SavingClickCoords[0], SavingClickCoords[1], evt.GetPosition().x, evt.GetPosition().y)


		if IsDrawing:
			Redraw()

	if IsPanelMoving == True:

		w, h = DrawScroller.GetSize()
		sw, sh = DrawPanel.GetSize()

		if w < sw or h < sh or SavingClickCoords[2] < 0 or SavingClickCoords[3] < 0 :

			curX, curY = GetMousePosition()
			difX, difY = curX-SavingClickCoords[0], curY-SavingClickCoords[1]
			newX, newY = SavingClickCoords[2]-difX, SavingClickCoords[3]-difY

			DrawScroller.Scroll(newX, newY)

def OnPenPropertyBrushSize(evt):
	global ContLine, CurrentToolSize, DrawingToolsTable

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

def ChangeAngle(evt):
	global CurrentAngle
	CurrentAngle = int(Polygon.GUI["UG"].GetValue())

def ChangeRadius(evt):
	global CurrentRadius
	CurrentRadius = int(RoundRect.GUI["AN"].GetValue())

def AtStart(evt):
	global DrawScroller
	DrawScroller.Scroll(0, 0)

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
	info.AddDeveloper("Максимов Павел Александрович\n(AriosJentu)\n[Б8103-а]")

	AboutBox(info)

def OnSelectPenStyle(evt):

	global PenStyles, CurrentPenStyle, DrawingToolsTable

	string = evt.GetString()
	string = string.encode("utf-8")

	for i in PenStyles:
		if i[0] == string:
			CurrentPenStyle = i[1]
			break


	for i in DrawingToolsTable:
		i.GUI["SP"].SetValue(string)

def OnSelectBrushStyle(evt):

	global BrushStyles, CurrentBrushStyle, DrawingToolsTable, ContLine, Line

	string = evt.GetString()
	string = string.encode("utf-8")

	for i in BrushStyles:
		if i[0] == string:
			CurrentBrushStyle = i[1]

	for i in DrawingToolsTable:
		if i != ContLine and i != Line:
			i.GUI["SB"].SetValue(string)

def OnPaintChangeScale(evt, source):

	global CurrentToolSize, CurrentZoom, Figures

	newScale = source.GetValue()

	divParam = float(newScale)/float(CurrentZoom)

	CurrentToolSize = CurrentToolSize*divParam

	for i in Figures:
		
		i.BrushSize = i.BrushSize*divParam

		for j, k in enumerate(i.Points):
			k[0] = k[0]*divParam
			k[1] = k[1]*divParam

	Redraw(True)

	CurrentZoom = newScale

def OnClickScale(evt, but):

	global DrawScroller, CurrentZoom, IsLoop, Paint, ScalingArguments
	IsLoop = False

	ax, ay, w, h = ScalingArguments

	x, y = DrawScroller.GetViewStart()
	a, b = evt.GetPosition()

	if abs(ax-w) < 10 and abs(ay-h) < 10:
		
		dif = 10 if but == "in" else -10
		PrevZoom = CurrentZoom
		Loop.GUI["LP"].SetValue( Loop.GUI["LP"].GetValue() + dif )

		x = a-x
		y = b-y

	else:

		dep = float(
				max( 
					float(100*Paint.MinW/abs(ax-w)), 
					float(100*Paint.MinH/abs(ay-h)) 
				)/100
			) if but == "in" else float(
				min( 
					float(100*abs(ax-w)/Paint.MinW), 
					float(100*abs(ay-h)/Paint.MinH) 
				)/100
			)


		NewScale = int( CurrentZoom*dep )
		NewScale = 500 if NewScale>500 else 20 if NewScale < 20 else NewScale
		#print(NewScale)

		x = ax*(NewScale/CurrentZoom)
		y = ay*(NewScale/CurrentZoom)

		Loop.GUI["LP"].SetValue(NewScale)

	OnPaintChangeScale(evt, Loop.GUI["LP"])

	DrawScroller.Scroll(x, y)

def OnPaintDef(evt, tst):
	global CurrentTool, Loop

	if CurrentTool == Loop:
		OnClickScale(evt, tst)
	else:
		OnPaintMouseUp(evt)


PaintFrame.Bind(EVT_SIZE, OnFrameResize)
PaintFrame.Bind(EVT_CLOSE, OnQuit)

FileMenu.Bind(EVT_MENU, OnQuit, id=ID_EXIT)
FileMenu.Bind(EVT_MENU, Undo, id=ID_UNDO)
FileMenu.Bind(EVT_MENU, Redraw, id=ID_REDRAW)
FileMenu.Bind(EVT_MENU, ClearPaint, id=ID_CLEAR)

HelpMenu.Bind(EVT_MENU, ShowAbout, id=ID_ABOUT)

DrawPanel.Bind(EVT_PAINT, OnPaint)
DrawPanel.Bind(EVT_LEFT_DOWN, lambda evt: OnPaintMouseDown(evt, "left") )
DrawPanel.Bind(EVT_RIGHT_DOWN, lambda evt: OnPaintMouseDown(evt, "right") )
DrawPanel.Bind(EVT_MIDDLE_DOWN, lambda evt: OnPaintMouseDown(evt, "middle") )
DrawPanel.Bind(EVT_LEFT_UP, lambda evt: OnPaintDef(evt, "in") )
DrawPanel.Bind(EVT_RIGHT_UP, lambda evt: OnPaintDef(evt, "out") )
DrawPanel.Bind(EVT_MIDDLE_UP, OnPaintMouseUp)
DrawPanel.Bind(EVT_MOTION, OnPaintMouseMove)

for i in DrawingToolsTable:
	i.GUI["BS"].Bind(EVT_SPINCTRL, OnPenPropertyBrushSize)
	i.GUI["SP"].Bind(EVT_COMBOBOX, OnSelectPenStyle)
	if i != ContLine and i != Line:
		i.GUI["SB"].Bind(EVT_COMBOBOX, OnSelectBrushStyle)

Polygon.GUI["AN"].Bind(EVT_SPINCTRL, ChangePolygons)
Polygon.GUI["UG"].Bind(EVT_SPINCTRL, ChangeAngle)

RoundRect.GUI["AN"].Bind(EVT_SPINCTRL, ChangeRadius)

Move.GUI["ST"].Bind(EVT_LEFT_DOWN, AtStart)
Loop.GUI["LP"].Bind(EVT_SPINCTRL, lambda evt: OnPaintChangeScale(evt, evt.GetEventObject()) )

Loop.GUI["LP"].SetValue(100)
RoundRect.GUI["AN"].SetValue(5)
