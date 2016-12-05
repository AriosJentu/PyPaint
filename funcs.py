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
		
		self.Panel = ScrolledWindow(parent, ID_ANY)
		self.Panel.SetScrollRate(5, 5)
		self.Panel.EnableScrolling(True, True)

		self.Panel.SetSize(parent.GetSize())
		self.Panel.Move(Point(0, 1))

		self.Panel.SetBackgroundColour(color)

		self.Property = {}
		self.Labels = {}
		Slide = BoxSizer(VERTICAL)
		Slide.AddSpacer(5)

		self.PSize = 0

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
				#self.Property[key].SetBackgroundColour(color)
				#self.Property[key].SetForegroundColour(Colour(255, 255, 255))

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

def checkInRound(x, y, w, h, radW, radH, cenX, cenY):
	try:
		t1 = ( ( float(abs(w-cenX)**2)/(radW**2) + float(abs(h-cenY)**2)/(radH**2) ) < 1 )
		t2 = ( ( float(abs(x-cenX)**2)/(radW**2) + float(abs(h-cenY)**2)/(radH**2) ) < 1 )
		t3 = ( ( float(abs(w-cenX)**2)/(radW**2) + float(abs(y-cenY)**2)/(radH**2) ) < 1 )
		t4 = ( ( float(abs(x-cenX)**2)/(radW**2) + float(abs(y-cenY)**2)/(radH**2) ) < 1 )
		return t1 or t2 or t3 or t4
	except:
		return True

def SelectFiguresInRange(x, y, w, h):
	for i in Figures:	
	
		x, w = min(x, w), max(x, w)
		y, h = min(y, h), max(y, h)
	
		if i.Tool.Continious:
			for j in i.Points:

				if w > j[0] > x and h > j[1] > y:
					i.Selected = True
					break
				else:
					i.Selected = False
		else:
			
			ax, ay, bx, by = i.Points[0][0], i.Points[0][1], i.Points[1][0], i.Points[1][1]

			check1 = ( ( x <= ax <= w or x <= bx <= w ) and ( y <= ay <= h or y <= by <= h ) )
			check2 = ( 
				( ax <= x <= bx or ay <= y <= by ) and ( ax <= w <= bx or ay <= h <= by ) 
			) and ( 
				( x <= ax <= w or y <= ay <= h ) or ( x <= bx <= w or y <= by <= h ) 
			) 
			

			if i.Tool.Name == "Rectangle":
				
				i.Selected = True if check1 or check2 else False

			elif i.Tool.Name == "Ellipse":
				radW = abs(ax - bx)	/ 2
				radH = abs(ay - by)	/ 2	
				cenX = ax+radW
				cenY = ay+radH

				check1 = (( x > ax and w < bx ) and ( y <= ay and h >= by )) or (( y > ay and h < by ) and ( x <= ax and w >= bx ))
				check2 = checkInRound(x, y, w, h, radW, radH, cenX, cenY)
				check3 = ( x <= ax and y <= ay and w >= bx and h >= by )
				i.Selected = True if check1 or check3 or check2 else False

			else:

				i.Selected = True if check1 or check2 else False

