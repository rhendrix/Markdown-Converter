#!/usr/bin/env python3

#File containing the markdown classes

class Header:
	type = "Header"
	def __init__(self, headerLevel, text):
		self.headerLevel = headerLevel
		self.text = text
		return
	
	def __repr__(self):
		return "Header: {0}, \"{1}\"".format(self.headerLevel, self.text)

class List:
	type = "List"
	def __init__(self, ordered):
		self.ordered = ordered
		self.items = []
		return

	def __repr__(self):
		return "List: {0}, {1}".format(self.ordered, len(self.items))

	def append(self, item):
		self.items.append(item)

class Item:
	type = "Item"
	def __init__(self, par, parent):
		self.paragraph = par
		self.items = []
		self.parent = parent
		return

	def __repr__(self):
		return "Item: \"{0}\"".format(len(self.items))

	def append(self, item):
		self.items.append(item)

class Image:
	type = "Image"
	def __init__(self, altText, url, scale="100%"):
		self.altText = altText
		self.url = url
		self.scale = scale
		return

	def __repr__(self):
		return "Image: \"{0}\", \"{1}\", {2}".format(self.url, self.altText, self.scale)

class Link:
	type = "Link"
	def __init__(self, text, url):
		self.text = text
		self.url = url
		return

	def __repr__(self):
		return "Link: \"{0}\", \"{1}\"".format(self.url, self.text)

class Paragraph:
	type = "Paragraph"
	def __init__(self):
		self.textItems = []
		return

	def __repr__(self):
		str = ""
		for t in self.textItems:
			str = str + t.__repr__()
		return str

	def append(self, textItem):
		self.textItems.append(textItem)

class Text:
	type = "Text"
	def __init__(self, text, bold=False, it=False, code=False):
		self.text = text
		self.bold = bold
		self.it = it
		self.code = code	
		return

	def __repr__(self):
		t = "Text: "
		if self.bold:
			t += "Bold "
		if self.it:
			t += "It "
		if self.code:
			t += "Code "
		t += "\n"
		t += self.text
		return t

class Table:
	type = "Table"
	def __init__(self):
		self.table = []
		return

	def __repr__(self):
		align = ""
		for c in self.table:
			align = align + c[0]
		return "Table: " + align + ", (" + str(len(self.table)) + ", " + str(len(self.table[0])) + ")"

	def addColumn(self, align, head):
		self.table.append([])
		self.table[-1].append(align)
		self.table[-1].append(head)
		return
	
	def addCell(self, text, col):
		self.table[col].append(text)
		return

class CodeBlock:
	type = "Code Block"
	def __init__(self, lang=""):
		self.lines = []
		self.lang = lang

	def __repr__(self):
		code = ""
		for line in self.lines:
			code = code + line + "\n"
		return "Code:\n" + code[:-1]

	def addLine(self, line):
		self.lines.append(line)
		return
