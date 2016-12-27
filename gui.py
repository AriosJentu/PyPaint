# -*- encoding: utf-8 -*-
from wx.combo import BitmapComboBox

iconDir = APPDIR+"icons/logo.png"

#Окно
PaintFrame = Frame(None, ID_ANY, "Графический редактор")
PaintFrame.Center()
PaintFrame.SetSize(Size(800, 600))
PaintFrame.Show(True)
PaintFrame.SetBackgroundColour(Colour(255, 255, 255))
PaintFrame.SetIcon(Icon(iconDir))

#Меню
PaintMenu = MenuBar()

ID_UNDO, ID_REDO, ID_REDRAW, ID_CLEAR, ID_EXIT, ID_OPEN, ID_SAVE, ID_SAVEAS, ID_NEW = 100, 101, 102, 103, 104, 105, 106, 107, 108
ID_ABOUT = 200

FileMenu = Menu()
FileMenu.Append(ID_NEW, "Создать")
FileMenu.Append(ID_OPEN, "Открыть")
FileMenu.Append(ID_SAVE, "Сохранить")
FileMenu.Append(ID_SAVEAS, "Сохранить как")
FileMenu.AppendSeparator()
UndoItem = FileMenu.Append(ID_UNDO, "Отменить")
RedoItem = FileMenu.Append(ID_REDO, "Повторить")
FileMenu.AppendSeparator()
FileMenu.Append(ID_REDRAW, "Перерисовать")
FileMenu.Append(ID_CLEAR, "Очистить")
FileMenu.AppendSeparator()
FileMenu.Append(ID_EXIT, "Выход")

HelpMenu = Menu()
HelpMenu.Append(ID_ABOUT, "О программе")

PaintMenu.Append(FileMenu, "Файл")
PaintMenu.Append(HelpMenu, "Помощь")
UndoItem.Enable(False)
RedoItem.Enable(False)

PaintFrame.SetMenuBar(PaintMenu)


#Панель инструментов и свойств
PaintSidePanel = Panel(PaintFrame, -1)
PaintSidePanel.SetSize(Size(115, 600-51))
PaintSidePanel.Move(Point(0, 0))
PaintSidePanel.SetBackgroundColour(Colors["Default"])

#Панель рисования
DrawScroller = ScrolledWindow(PaintFrame, ID_ANY)
DrawScroller.SetScrollbars(1, 1, 800-115, 600-51)

DrawScroller.SetSize(Size(685, 600-51))
DrawScroller.Move(Point(115, 0))
DrawScroller.SetBackgroundColour(Colour(255, 255, 255))

DrawPanel = Panel(DrawScroller, ID_ANY)
DrawPanel.SetSize(Size(685, (600-51) ))
DrawPanel.Move(Point(0, 0))
DrawPanel.SetBackgroundColour(Colour(255, 255, 255))

Paint = PaintZone(DrawPanel)
Paint.Clear()

PaintButtons = []
CurrentProperty = None

n = len(Tools)+1
n = int(n/2)+1 if int(n/2) <= n/2 else int(n/2)

PaintParameters = Panel(PaintSidePanel, ID_ANY)
PaintParameters.SetSize(Size(114, 600-(n*55)-56))
PaintParameters.Move(Point(0, n*55+5))
PaintParameters.SetBackgroundColour(Colors["Panel"])

DividerPanel = Panel(PaintParameters, ID_ANY)
DividerPanel.SetSize(Size(114, 1))
DividerPanel.Move(Point(0, 0))
DividerPanel.SetBackgroundColour("#333333")

ColorBar = []
ColorBar.append(Button(PaintSidePanel, ID_ANY) )
ColorBar[0].SetSize(Size(50, 30))
ColorBar[0].Move(Point(5, (n-1)*55+5))
ColorBar[0].SetBackgroundColour(Colour(0, 0, 0))

ColorBar.append(Button(PaintSidePanel, ID_ANY) )
ColorBar[1].SetSize(Size(50, 30))
ColorBar[1].Move(Point(60, (n-1)*55+5))
ColorBar[1].SetBackgroundColour(Colour(255, 255, 255))

pane = Panel(PaintSidePanel, ID_ANY)
pane.SetSize(Size(105, 22))
pane.SetForegroundColour(Colors["Default"])
pane.SetBackgroundColour(Colors["Default"])
sizer = BoxSizer(HORIZONTAL)

label = StaticText(pane, ID_ANY)
label.SetLabel("Свойства:")
label.SetSize(Size(105, 22))
label.Move(Point(0, 0))
label.SetForegroundColour(Colour(255, 255, 255))

sizer.Add(label)
pane.SetSizer(sizer)
sizer.Fit(pane)
pane.Centre()
pane.Move(Point(pane.GetPosition().x, (n-1)*55+40))

PaintFrame.SetMinSize(Size(640, (n+5)*55))

def OnColorClick(evt):
	global SavingColours
	source = evt.GetEventObject()

	idd = 1 if source == ColorBar[1] else 0

	colBar = ColorBox(PaintFrame, source.GetBackgroundColour())

	if colBar.ShowModal() == ID_OK:
	
		data = colBar.GetColourData()
		r, g, b = data.GetColour()
		col = "#"+ToHEX(r, g, b)
	
		source.SetBackgroundColour(col)
		CurrentColour[idd] = col

		for i in xrange(16):
			r, g, b = data.GetCustomColour(i)
			SavingColours[i] = "#"+ToHEX(r, g, b)

		for i in Figures:
			if i.Selected:
				if idd == 0:
					i.PenColor = col
				else:
					i.BrushColor = col
		Redraw()

		colBar.Destroy()

for i in ColorBar:
	i.Bind(EVT_LEFT_DOWN, OnColorClick)


class PaintButton:

	def __init__(self, tool):
		
		n = len(PaintButtons)

		x = 60
		if n%2 == 0:
			x = 5
		y = int(n/2)*55 + 5

		self.Tool = tool

		color = Colors["Click"] if CurrentTool == self.Tool else Colors["Default"]

		self.But = BitmapButton(PaintSidePanel, -1, Bitmap(self.Tool.Icon))
		self.But.Move(Point(x, y))
		self.But.SetSize(Size(50, 50))
		self.But.SetBackgroundColour(color)

		self.But.Bind(EVT_ENTER_WINDOW, self.onEnterButtons)
		self.But.Bind(EVT_LEAVE_WINDOW, self.onLeaveButtons)
		self.But.Bind(EVT_LEFT_UP, self.onClickBut)

		self.But.SetToolTip(ToolTip(self.Tool.Rus))

		self.PropList = ObjectProperties(PaintParameters, self.Tool.Properties)
		self.PropList.Visible(False if CurrentTool != self.Tool else True)

		self.Tool.GUI = self.PropList.Property

	def onEnterButtons(self, evt):
		self.But.SetBackgroundColour(Colors["Enter"])

	def onLeaveButtons(self, evt):
		color = Colors["Click"] if CurrentTool == self.Tool else Colors["Default"]
		self.But.SetBackgroundColour(color)

	def onClickBut(self, evt):

		global CurrentTool, CurrentProperty

		CurrentTool = self.Tool

		for v in Tools:
			if v["tool"] == CurrentTool:
				Paint.SetTool(v["name"])
				break

		for j in PaintButtons:
			j.But.SetBackgroundColour(Colors["Default"])
			j.PropList.Visible(False)

		self.But.SetBackgroundColour(Colors["Click"])

		CurrentProperty = self.PropList
		self.PropList.Visible(True)



for v in Tools:
	PaintButtons.append(PaintButton(v["tool"]))