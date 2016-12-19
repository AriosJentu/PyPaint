# -*- encoding: utf-8 -*-
"""
###FILE EXAMPLE:###

@Signature

$classname:
- Attribute: 12;
- Attribute: Solid;
$end

$classname:
- Attribute: 12;
- Attribute: Solid;
$end

@Finish
"""
#Signature = "PyPaintAriJen"

def isNumber(txt):
	try:
		if str(type(int(txt))).find("int") != -1:
			return True
		else:
			return False
	except:
		return False

def saveFile(dirs):
	global Figures, Signature

	output = "@"+Signature

	for i in Figures:
		
		tabOfAttributes = [j for j in dir(i) if j[:2] != "__" and str(type(getattr(i, j))).find("instance") == -1]
		
		output += "\n\n$" + (i.__class__.__name__) + ":\n"
		
		#print(tabOfAttributes)
		
		for j in tabOfAttributes:
			attr = j
			attrval = getattr(i, j)
			output += "- "+attr+": "+str(attrval)+";\n"

		output += "$end"

	output += "\n\n@Finish"
	#print(output)

	outputFile = open(dirs, "w+")
	outputFile.write(output)
	outputFile.close()

def openFile(dirs):
	global Figures, Signature, ClassList

	inputFile = open(dirs, "r+")
	inputText = inputFile.read()
	inputFile.close()

	fileStart = inputText.find("@"+Signature)
	fileEnd = inputText.find("@Finish")

	if fileStart == -1 or fileEnd == -1:
		MessageDialog(None, "Ошибка загрузки файла:\nНе найдены сигнатуры", "Ошибка", OK | ICON_ERROR).ShowModal()
		#print("Не найдены сигнатуры")
		return False

	inputText = inputText[fileStart:fileEnd+7]
	thisClassEnd = inputText.find("$end")

	Figures = []

	IsAnyErrors = False

	while thisClassEnd != -1:

		classNameStart = inputText.find("$")+1
		classNameEnd = inputText.find(":")

		if classNameStart == 1 and classNameEnd != -1 and (inputText[:classNameEnd].find("-") != -1 or inputText[:classNameEnd].find("\n") != -1): 
			inputText = inputText[thisClassEnd+4:]
			thisClassEnd = inputText.find("$end")

			if thisClassEnd == -1:
				break

		className = inputText[classNameStart:classNameEnd]

		allThisClass = inputText[classNameEnd+1:thisClassEnd]

		classAttributes = {}

		while allThisClass.find("- ") != -1:

			thisAttrNameStart = allThisClass.find("- ")+2
			thisAttrNameEnd = allThisClass.find(":")
			thisAttrFinish = allThisClass.find(";")+1

			thisAttributeName = allThisClass[thisAttrNameStart:thisAttrNameEnd]
			thisAttributeValue = allThisClass[thisAttrNameEnd+2:thisAttrFinish-1]

			if thisAttrNameStart != 1 and thisAttrNameEnd != -1 and thisAttrFinish != 0 and (thisAttrNameStart < thisAttrNameEnd < thisAttrFinish):
				classAttributes[thisAttributeName] = thisAttributeValue
				allThisClass = allThisClass[thisAttrFinish:]
			else:
				ending = allThisClass.find("\n")
				allThisClass = allThisClass[ending+1:]
				IsAnyErrors = True

			#print(allThisClass, thisAttrNameStart, thisAttrNameEnd, thisAttrFinish, allThisClass.find("\n"))

		inputText = inputText[thisClassEnd+4:]
		thisClassEnd = inputText.find("$end")

		#print("###############################")
		#print(inputText)
		#print("###############################")
		#print(className)
		#print(classAttributes)
		#print(" ")
		
		inst = getattr(ClassList, className)
		figClass = inst()
		for i, v in classAttributes.items():

			if v == "True" or v == "False":
				
				v = True if v == "True" else False

			elif v.find("[") != -1:
				
				v = v.replace("[", "").replace("]", "")
				x = [int(k) for k in v.split(", ")]
				v = []				
				for j in range(0, len(x), 2):
					v.append([ x[j], x[j+1] ])
			
			elif isNumber(v):
			
				v = int(v)
			
			#print(i, v)

			setattr(figClass, i, v)

	if IsAnyErrors:
		MessageDialog(None, "В процессе загрузки произошли ошибки\nВозможно не все данные будут отображены\nна экране", "Ошибка", OK | ICON_ERROR).ShowModal()


#openFile("example.ajp")