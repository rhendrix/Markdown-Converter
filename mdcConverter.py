#!/usr/bin/env python3

from mdcClasses import *

#File containing routines to convert from tokens to
#markdown classes

#returns list of markdown objects
#tokens is the list of tokens from tokenize
def tokensToObjects(tokens):
	objects = []	
	i = 0
	while i < len(tokens):
		if tokens[i].type == "Header":
			objects.append(header(tokens[i]))
		elif tokens[i].type == "Image":
			objects.append(image(tokens[i]))
		elif tokens[i].type == "Text":
			i = paragraph(i, tokens, objects)
			continue
		elif tokens[i].type == "List":
			i = list(i, tokens, objects)
			continue
		elif tokens[i].type == "Table":
			i = table(i, tokens, objects)
			continue
		elif tokens[i].type == "Code Block":
			i = codeblock(i, tokens, objects)
			continue
		i = i + 1		
	return objects	

#returns a header object
#tok is the header token to be converted
def header(tok):
	count = 0
	for c in tok.line:
		if c == "#":
			count = count + 1
		else:
			break
	return Header(count, tok.line[count+1:])

#returns an image object
#tok is the image token to be converted
def image(tok):
	altStart = 2
	altEnd = tok.line.find("](")
	altText = tok.line[altStart:altEnd]

	urlStart = altEnd + 2
	if tok.line[-2] == "%":
		urlEnd = tok.line.rfind(" ")
		url = tok.line[urlStart:urlEnd]

		scaleStart = urlEnd + 1
		scaleEnd = -1
		scale = tok.line[scaleStart:scaleEnd]
		obj = Image(altText, url, scale=scale)
	else:
		urlEnd = -1
		url = tok.line[urlStart:urlEnd]

		obj = Image(altText, url)
		
	return obj

#returns a link object
#tok is the link token to be converted
def link(tok):
	textStart = 1
	textEnd = tok.line.find("](")
	text = tok.line[textStart:textEnd]

	urlStart = textEnd + 2
	urlEnd = -1
	url = tok.line[urlStart:urlEnd]

	return Link(text, url)

#Creates Paragraph object and appends to objects list
#returns updated token list index
#i is the current token list index
#tokens is the token list
#objects is the object list
def paragraph(i, tokens, objects):
	par = Paragraph()
	bold = False
	it = False
	code = False
	ignore = False
	skip = False

	prev = ""
	text = ""

	while tokens[i].type == "Text":
		for x, c in enumerate(tokens[i].line):
			if c == '\\' and not ignore:
				ignore = True
			elif skip:
				skip = False
				continue
			elif c == '*' and not ignore and not code:
				#Append existing text if it's not empty
				if text != "":
					par.append(Text(text, bold=bold, it=it, code=code))
					text = ""
				#Toggle bold or it depending on stars
				if x+1 < len(tokens[i].line):
					if tokens[i].line[x+1] == "*":
						bold = not bold
						skip = True
					else:
						it = not it
				else:
					it = not it
			elif c == '_' and not ignore and not code:
				if text != "":
					par.append(Text(text, bold=bold, it=it, code=code))
					text = ""
				if x+1 < len(tokens[i].line):
					if tokens[i].line[x+1] == "_":
						bold = not bold
						skip = True
					else:
						it = not it
				else:
					it = not it
			elif c == '`' and not ignore:
				if text != "":
					par.append(Text(text, bold=bold, it=it, code=code))
					text = ""
				code = not code
			elif c == "[" and not ignore and not code:
				if text != "":
					par.append(Text(text, bold=bold, it=it, code=code))
					text = ""
			elif c == "]" and not ignore and not code:
				prev = text
				text = ""
			elif c == "(" and not ignore and not code:
				continue
			elif c == ")" and not ignore and not code:
				par.append(Link(prev, text))
				text = ""
				prev = ""
			else:
				text = text + c
				ignore = False
		if text != "":
			par.append(Text(text, bold=bold, it=it, code=code))
			text = ""
		if i+1 == len(tokens):
			i = i + 1
			break
		i = i + 1	
	objects.append(par)
	return i 

#returns new paragraph made from string
#line is the string to convert
def strToPar(line):
	par = Paragraph()
	bold = False
	it = False
	code = False
	ignore = False
	skip = False

	prev = ""
	text = ""

	for x, c in enumerate(line):
		if c == '\\' and not ignore:
			ignore = True
		elif skip:
			skip = False
			continue
		elif c == '*' and not ignore and not code:
			#Append existing text if it's not empty
			if text != "":
				par.append(Text(text, bold=bold, it=it, code=code))
				text = ""
			#Toggle bold or it depending on stars
			if x+1 < len(line):
				if line[x+1] == "*":
					bold = not bold
					skip = True
				else:
					it = not it
			else:
				it = not it
		elif c == '_' and not ignore and not code:
			if text != "":
				par.append(Text(text, bold=bold, it=it, code=code))
				text = ""
			if x+1 < len(tokens[i].line):
				if line[x+1] == "_":
					bold = not bold
					skip = True
				else:
					it = not it
			else:
				it = not it
		elif c == '`' and not ignore:
			if text != "":
				par.append(Text(text, bold=bold, it=it, code=code))
				text = ""
			code = not code
		elif c == "[" and not ignore and not code:
			if text != "":
				par.append(Text(text, bold=bold, it=it, code=code))
				text = ""
		elif c == "]" and not ignore and not code:
			prev = text
			text = ""
		elif c == "(" and not ignore and not code:
			continue
		elif c == ")" and not ignore and not code:
			par.append(Link(prev, text))
			text = ""
			prev = ""
		else:
			text = text + c
			ignore = False
	if text != "":
		par.append(Text(text, bold=bold, it=it, code=code))
		text = ""
	return par

#creates List object and appends to objects list
#returns updated token list index
#i is the current token list index
#tokens is the token list
#objects is the object list
def list(i, tokens, objects):
	if tokens[i].line[0] == '*':
		li = List(False)
	else:
		li = List(True)

	curPar = li
	curTabs = 0
	while tokens[i].type == "List":
		tabs = tabCount(tokens[i].line)
		if tabs == curTabs:
			sp = tokens[i].line.find(" ")
			text = strToPar(tokens[i].line[sp+1:])
			curPar.append(Item(text, curPar))
			if i+1 == len(tokens):
				break
			i = i + 1
		elif tabs > curTabs:
			curTabs = tabs
			curPar = curPar.items[-1]
		elif tabs < curTabs:
			dif = curTabs - tabs
			curTabs = tabs
			for j in range(0, dif):
				curPar = curPar.parent
	objects.append(li)
	return i 

#returns the number of tabs in line
#line the line to search
def tabCount(line):
	count = 0
	for c in line:
		if c == "\t":
			count = count + 1
		else:
			break
	return count

#creates Table object and appends to objects list
#returns updated token list index
#i is the current token list index
#tokens is the token list
#objects is the object list
def table(i, tokens, objects):
	tab = Table()

	cols = tokens[i].line.count(" | ") + 1
	headCells = tokens[i].line.split(" | ")
	alignCells = tokens[i+1].line.split(" | ")
	
	for x in range(0, cols):
		head = headCells[x].strip()
		align = getAlign(alignCells[x].strip())
		tab.addColumn(align, head)

	i = i + 2
	while tokens[i].type == "Table":
		cells = tokens[i].line.split(" | ")
		for x in range(0, cols):
			tab.addCell(cells[x].strip(), x)
		if i+1 == len(tokens):
			break
		i = i + 1
	objects.append(tab)
	return i 

#returns the text alignment of a column based on the given cell
#cell is the alignment cell from a markdown table column
def getAlign(cell):
	if cell.count(":") == 2:
		return "center"
	elif cell[0] == ":":
		return "left"
	else:
		return "right"

#creates CodeBlock object and appends to objects list
#returns updated token list index
#i is the current token list index
#tokens is the token list
#objects is the object list
def codeblock(i, tokens, objects):
	lang = tokens[i].line[3:]
	cb = CodeBlock(lang)
	i = i + 1
	while tokens[i].type != "Code Block":
		line = str.replace(tokens[i].line, "\`", "`")
		cb.addLine(line)
		i = i + 1
	objects.append(cb)
	return i + 1
