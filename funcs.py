# -*- encoding: utf-8 -*-
#Конверторы:
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
				self.Property[key] = ComboBox(self.Panel, ID_ANY, style=CB_READONLY, choices=val[0], size=(100,30))
				self.Property[key].SetValue(str(val[0]))
				self.Property[key].SetBackgroundColour(color)
				self.Property[key].SetForegroundColour(Colour(255, 255, 255))

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


