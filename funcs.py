# -*- encoding: utf-8 -*-
#Конверторы:

from wx.combo import BitmapComboBox

def ToRGB(c):
	if len(c) == 8:
		return int(c[6:8], 16), int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
	elif len(c) == 6:
		return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

def ToHEX(*args):
	res = ""
	for i in args:
		res = res+"%.2x"%i

	return res

#tabOfProps = {"name":[1, 2, 3, 4], "namz":["lab", 12, "123"]}
#Get property gui-element from Tool: Tool.GUI["PropName"]
class ObjectProperties:	

	def __init__(self, parent, tabOfProps):
		
		color = Colors["Panel"]
		
		self.Parent = parent
		self.Panel = ScrolledWindow(self.Parent, ID_ANY)
		self.Panel.SetScrollRate(5, 5)
		self.Panel.EnableScrolling(True, True)

		self.Panel.SetSize(self.Parent.GetSize())
		self.Panel.Move(Point(0, 1))

		self.Panel.SetBackgroundColour(color)

		self.Property = {}
		self.Labels = {}
		Slide = BoxSizer(VERTICAL)
		Slide.AddSpacer(5)

		self.PSize = 0
		CreatePropsFromTable(self, tabOfProps)

	def CreatePropsFromTable(self, tabOfProps):

		for key, val in tabOfProps.items():

			types = "spin"

			if type(val[0]) != type([]):
				types = "btn"
				self.BtnEvent = {}
			else:
				for value in val[0]:
					if str(type(value)).find("str") != -1:
						types = "cb"
						break

			self.Labels[key] = StaticText(self.Panel, ID_ANY, str(val[1])+":", size=(100, 20))
			self.Labels[key].SetForegroundColour(Colour(255, 255, 255))

			if types == "spin":
				self.Property[key] = SpinCtrl(self.Panel, ID_ANY, size=(100,30))
				self.Property[key].SetRange(int(min(val[0])), int(max(val[0])))
				self.Property[key].SetBackgroundColour(color)
				self.Property[key].SetForegroundColour(Colour(255, 255, 255))

			elif types == "btn":

				self.Property[key] = CustomButton(self.Panel, ID_ANY, str(val[0]), size=(100, 30))
				self.Property[key].Color = color
				self.Property[key].SetBackgroundColour(color)
			
			else:
				self.Property[key] = BitmapComboBox(self.Panel, ID_ANY, style=CB_READONLY, size=(100,30))
				
				tab = []
				for i in val[0]:
					tab.append([i])

				for i, v in enumerate(tab):
					try:
						if val[2][i]:
							v.append(val[2][i])
					except:
						v.append("none")

				for i in tab:
					self.Property[key].Append(i[0], Bitmap(APPDIR+"styles/"+i[1]+".png"))


				self.Property[key].SetValue(str(tab[0][0]))

			Slide.Add(self.Labels[key])
			Slide.Add(self.Property[key])
			Slide.AddSpacer(5)

			self.PSize += 55

		
		self.Panel.SetSizer(Slide)
		self.Panel.FitInside()

		for i, v in enumerate(self.Property):
			self.Labels[v].Move(Point(7, (i*55)+5))
			self.Property[v].Move(Point(7, (i*55)+25))

	def Visible(self, bol):
		self.Panel.Show(bol)

	def ClearProps(self):
		self.Panel.DestroyChildren()


class CustomButton(Button):

	def __init__(self, *args, **kwarg):
		Button.__init__(self, *args, **kwarg)
		self.Color = Colors["Default"]
		self.EnterColor = Colors["Enter"]
		self.Bind(EVT_ENTER_WINDOW, self.onEnterButtons)
		self.Bind(EVT_LEAVE_WINDOW, self.onLeaveButtons)

		self.SetBackgroundColour(self.Color)
		self.SetForegroundColour("#FFFFFF")

	def onEnterButtons(self, evt):
		self.SetBackgroundColour(self.EnterColor)

	def onLeaveButtons(self, evt):
		self.SetBackgroundColour(self.Color)

def IsPointInEllipse(x0, y0, x1, y1, radX, radY, cenX, cenY):
	result = False

	for i in xrange(x0, x1+1, 2):
		for j in xrange(y0, y1+1, 2):
			x = float((i-cenX)*(i-cenX))
			f = float(radX*radX) 
			y = float((j-cenY)*(j-cenY))
			g = float(radY*radY)
			if x*g - f*g + y*f <= 0:
			#if float((i-cenX)*(i-cenX))/float(radX*radX) + float((j-cenY)*(j-cenY))/float(radY*radY) <= 1.0:
				result = True
				break
		if result == True:
			break

	return result

def IsPointOnLine(spx, spy, epx, epy, x0, y0, x1, y1):
	result = False

	for i in xrange(spx, epx+1):
		for j in xrange(spy, epy+1):
			if min(x0, x1) <= i <= max(x0, x1) and min(y0, y1) <= j <= max(y0, y1):
				if (i-x0)*(y1-y0) - (j-y0)*(x1-x0) == 0:
					result = True
					break
		if result == True:
			break

	return result

def SelectFiguresInRange(x0, y0, x1, y1):
	tabOfSelected = []
	for i in Figures:
		check = i.IsRectIn(x0, y0, x1, y1)
		i.Selected = True if check else False
		
		if i.Selected:
			tabOfSelected.append(i.Tool.Name)

		



