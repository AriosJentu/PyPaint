# -*- encoding: utf-8 -*-
import math

Figures = []
Tools = []
Paint = None

PenStyles = [
	["Стандартный", SOLID, "sLine"],
	["Точечный", DOT, "sPPoint"],
	["Длинный Пунктир", LONG_DASH, "sLDash"],
	["Короткий Пунктир", SHORT_DASH, "sSDash"],
	["Пунктир-Точка", DOT_DASH, "sPDash"],
	["Без Границ", TRANSPARENT, "none"]
]
BrushStyles = [
	["Без Заливки", TRANSPARENT, "bTrans"],
	["Заливка", SOLID, "bSolid"],
	["Прямая Диагональ", FDIAGONAL_HATCH, "bFDiag"],
	["Обратная Диагональ", BDIAGONAL_HATCH, "bBDiag"],
	["Крестовое Пересечение", CROSSDIAG_HATCH, "bCross"],
	["Клетки", CROSS_HATCH, "bQuad"],
	["Вертикаль", VERTICAL_HATCH, "bVert"],
	["Горизонталь", HORIZONTAL_HATCH, "bHorz"]
]

CurrentTool = None
CurrentFigure = None

class PaintZone(PaintDC):

	def __init__(self, parent, *args, **kwar):
		PaintDC.__init__(self, parent, *args, **kwar)
		self.Func = self.DrawLine
		self.Name = "Pen"
		self.Parent = parent
		self.MinW, self.MinH = parent.GetSize()
		self.SavedOld = [0, 0]

		self.DefFuncs = {
			"Pen":self.DrawLine,
			"Line":self.DrawLine,
			"Rectangle":self.DrawRect,
			"Ellipse":self.DrawEll,
			"Polygon":self.DrawPolygon
		}

	def DrawFigure(self, figure):
		self.SetBrush(Brush(figure.BrushColor, figure.BrushStyle))
		self.SetPen(Pen(figure.PenColor, figure.BrushSize, figure.PenStyle))
		self.SetTool(figure.Tool.Name)

		if figure.Tool.Continious == True:

			for i, v in enumerate(figure.Points):

				if i+1 < len(figure.Points):

					if self.Name in self.DefFuncs:
						if self.Name == "Polygon":
							self.Func(v[0], v[1], figure.Points[i+1][0], figure.Points[i+1][1], figure.Polygons)
						else:
							self.Func(v[0], v[1], figure.Points[i+1][0], figure.Points[i+1][1])
		else:

			if self.Name in self.DefFuncs:
				mOld = figure.Points[0]
				mNew = figure.Points[1]
				
				if self.Name == "Polygon":
					self.Func(mOld[0], mOld[1], mNew[0], mNew[1], figure.Polygons)

				else:
					self.Func(mOld[0], mOld[1], mNew[0], mNew[1])

	def DrawRect(self, ax, ay, bx, by):

		x, y = min(ax, bx), min(ay, by)
		w, h = abs(ax-bx), abs(ay-by)

		self.DrawRectangle(x, y, w, h)	

	def DrawEll(self, ax, ay, bx, by):

		x, y = min(ax, bx), min(ay, by)
		w, h = abs(ax-bx), abs(ay-by)

		self.DrawEllipse(x, y, w, h)

	def DrawPolygon(self, ax, ay, bx, by, numOfAngles = 4):

		x, y = min(ax, bx), min(ay, by)
		w, h = abs(ax-bx), abs(ay-by)

		if numOfAngles < 3:
			numOfAngles = 3

		radiusW = w/2
		radiusH = h/2
		angle = 2*math.pi/numOfAngles
		x, y = x+radiusW, y+radiusH
		
		for i in xrange(numOfAngles):
			fx = radiusW*math.cos(angle*i)
			fy = radiusH*math.sin(angle*i)
			
			gx = radiusW*math.cos(angle*(i+1))
			gy = radiusH*math.sin(angle*(i+1))

			self.DrawLine(x+fx, y+fy, x+gx, y+gy)
		

	def SetTool(self, name):
		self.Name = name
		for i in Tools:
			if i["name"] == name:
				for j in self.DefFuncs.items():
					if i["name"] == j[0]:
						self.Func = self.DefFuncs[j[0]]
						break

	def CalcSizes(self):

		w, h = self.Parent.GetSize()
		wa, ha = self.Parent.GetParent().GetSize()

		MinCoordX, MinCoordY = 0, 0
		MaxCoordX, MaxCoordY = 0, 0

		for i in Figures:
			for j in i.Points:
				MinCoordX, MinCoordY = min(MinCoordX, j[0]-int(i.BrushSize/2)), min(MinCoordY, j[1]-int(i.BrushSize/2))

		if MinCoordX >= 0:
			MinCoordX = 0
		else:
			MinCoordX -= 8

		if MinCoordY >= 0:
			MinCoordY = 0
		else:
			MinCoordY -= 8

		for i in Figures:
			for j in i.Points:
				j[0] = j[0]-MinCoordX
				j[1] = j[1]-MinCoordY

		for i in Figures:
			for j in i.Points:
				MaxCoordX, MaxCoordY = max(MaxCoordX, j[0]+int(i.BrushSize/2)), max(MaxCoordY, j[1]+int(i.BrushSize/2))

		if MaxCoordX < wa+MinCoordX:
			MaxCoordX = wa+MinCoordX
		if MaxCoordY < ha+MinCoordY:
			MaxCoordY = ha+MinCoordY

		self.MinW, self.MinH = MaxCoordX+8, MaxCoordY+8

		if self.MinW < wa:
			self.MinW = wa
		if self.MinH < ha:
			self.MinH = ha

		self.Parent.Move(Point(0, 0))
		x, y = self.Parent.GetParent().GetViewStart()

		self.Parent.SetSize(Size(self.MinW, self.MinH))
		self.Parent.GetParent().SetScrollbars(1, 1, self.MinW, self.MinH)
		self.Parent.GetParent().Scroll(x+abs(MinCoordX)+self.SavedOld[0], y+abs(MinCoordY)+self.SavedOld[1])

		self.SavedOld = [abs(MinCoordX), abs(MinCoordY)]

SavingColours = [
	"#FF0000", "#00FF00", "#0000FF", "#4444FF", 
	"#6600FF", "#143F72", "#FF9900", "#18C018", 
	"#C01818", "#1818C0", "#D73030", "#30D730", 
	"#FFFFFF", "#000000", "#333333", "#444444"
]

class ColorBox(ColourDialog):

	def __init__(self, parent, colourD):
		global SavingColours 

		data = ColourData()
		data.SetColour(colourD)

		for i in xrange(16):
			data.SetCustomColour(i, SavingColours[i])


		ColourDialog.__init__(self, parent, data)

	def GetColor(self):
		r, g, b = self.GetColourData().GetColour()
		return "#"+ToHEX(r, g, b)

class Figure:

	def __init__(self):

		self.Points = []
		self.Tool = None
		self.PenColor = None
		self.BrushColor = None
		self.BrushSize = None
		self.Polygons = 3
		self.PenStyle = SOLID
		self.BrushStyle = TRANSPARENT

		Figures.append(self)

class Tool:

	def __init__(self, name, rname):
		self.Name = name
		self.Rus = rname
		self.Continious = False 
		self.IsDrawTool = True
		self.Icon = APPDIR+"icons/def.png"
		self.Properties = {}
		self.GUI = None

		Tools.append({"name":name, "tool":self})

	def AddProperty(self, name, rus, tableOfVariaties, tableOfImages = []):
		self.Properties[name] = [tableOfVariaties, rus, tableOfImages]


ContLine 				= Tool("Pen", "Кисть")
ContLine.Continious 	= True
ContLine.Icon 			= APPDIR+"icons/brush.png"

Move 					= Tool("Move", "Перемещение")
Move.Icon 				= APPDIR+"icons/move.png"
Move.IsDrawTool 		= False

Line 					= Tool("Line", "Линия")
Line.Icon 				= APPDIR+"icons/line.png"

Rectangle				= Tool("Rectangle", "Прямоугольник")
Rectangle.Icon			= APPDIR+"icons/rectangle.png"

Ellipse					= Tool("Ellipse", "Эллипс")
Ellipse.Icon			= APPDIR+"icons/ellipse.png"

Polygon					= Tool("Polygon", "Многоугольник")
Polygon.Icon 			= APPDIR+"icons/polygon.png"

Loop					= Tool("Scale", "Лупа")
Loop.Icon 				= APPDIR+"icons/zoom.png"
Loop.IsDrawTool 		= False

CurrentTool = ContLine

DrawingToolsTable = [ContLine, Line, Rectangle, Ellipse, Polygon]

#Example:
#Line.AddProperty("Scales", "Nothionk")				#For BUTTON
#Line.AddProperty("Scaled", ["12", "123", "1234"]) 	#For COMBOBOX
#Line.AddProperty("Scalen", [1, 2, 3, 4, 5])	 	#For SPINBOX

for i in DrawingToolsTable:
	i.AddProperty("BS", "Размер Кисти", [1, 60])
	i.AddProperty("SP", "Стиль Кисти", [j[0] for j in PenStyles], [j[2] for j in PenStyles])
	if i != ContLine and i != Line:
		i.AddProperty("SB", "Стиль Фигуры", [j[0] for j in BrushStyles], [j[2] for j in BrushStyles])
	

Polygon.AddProperty("AN", "Многоугольник", [3, 12])
Move.AddProperty("ST", "Перемещение", "В начало")

def onMoveClick():
	return False

def onLoopClick():
	return False

