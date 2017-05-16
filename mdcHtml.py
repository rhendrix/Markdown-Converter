#!/usr/bin/env python3

htmlHead = """<head>
	<style type=\"text/css\">
		body
		{
			margin: 40px auto;
			max-width: 650px;
			line-height: 1.6;
			font-size: 18px;
			background-color: #111111;
			color: #eeeeee;
			padding: 0 10px;
		}
		p
		{
			text-align: justify;
		}
		h1,h2,h3{line-height:1.2}
		a
		{
			color: #008080;
			text-decoration: none;
		}
		.inlineCode
		{
			font-family: monospace;
			outline: 2px solid #eeeeee;
		}
		.codeBlock
		{
			font-family: monospace;
			border: 2px solid #eeeeee;
			margin-top: 10px;
			margin-bottom: 10px;
		}
		table 
		{
			padding: 0; 
			border-spacing:0;
			border-collapse: collapse;
		}
		table tr 
		{
			background-color: #181818;
			margin: 0;
			padding: 0; 
		}
		table tr:nth-child(2n) 
		{
			background-color: #222222; 
		}
		table tr th 
		{
			background-color: #eeeeee;
			color: #111111;
			font-weight: bold;
			text-align: left;
			margin: 0;
			padding: 6px 13px; 
		}
		table tr td 
		{
			text-align: left;
			margin: 0;
			padding: 6px 13px; 
		}
		table tr th :first-child, table tr td :first-child 
		{
			margin-top: 0; 
		}
		table tr th :last-child, table tr td :last-child 
		{
			margin-bottom: 0; 
		}
		img
		{
			margin-top: 10; 
			margin-bottom: 10; 
		}
	</style>
</head>
"""

def toHtml(objects):
	html = ""
	html += "<DOCTYPE html>\n"
	html += "<html>\n"
	html += htmlHead
	html += "<body>\n"
	for o in objects:
		if o.type == "Header":
			html += headerToHtml(o)
		elif o.type == "Image":
			html += imageToHtml(o)
		elif o.type == "Paragraph":
			html += parToHtml(o)
		elif o.type == "List":
			html += listToHtml(o)
		elif o.type == "Table":
			html += tableToHtml(o)
		elif o.type == "Code Block":
			html += codeBlockToHtml(o)
	html += "</body>\n"
	html += "</html>"
	return html

def headerToHtml(obj):
	html = "<h{0} id=\"{1}\">{1}</h{2}>\n"
	html = html.format(obj.headerLevel, obj.text, obj.headerLevel)
	return html

def imageToHtml(obj):
	html = "<center><img src=\"{0}\" alt=\"{1}\" width=\"{2}\"></center>\n"
	html = html.format(obj.url, obj.altText, obj.scale)
	return html

def linkToHtml(obj):
	html = "<a href=\"{0}\">{1}</a>"
	html = html.format(obj.url, obj.text)
	return html

def parToHtml(obj):
	html = "<p>\n"
	for t in obj.textItems:
		if t.type == "Text":
			if t.bold:
				html += "<b>"
			if t.it:
				html += "<i>"
			if t.code:
				html += "<span class=\"inlineCode\">"

			newText = t.text
			newText = str.replace(newText, "<", "&lt;")
			newText = str.replace(newText, ">", "&gt;")
			html += newText

			if t.code:
				html += "</span>"
			if t.it:
				html += "</i>"
			if t.bold:
				html += "</b>"
		elif t.type == "Link":
			html += linkToHtml(t)
		html += "\n"
	html += "</p>\n"
	return html

def listToHtml(obj):
	return rlistToHtml(obj, obj.ordered, 0)

def rlistToHtml(obj, ordered, level):
	if len(obj.items) == 0:
		return ""
	html = ""
	if ordered:
		html += "<ol "+ getType(level) + ">\n"
	else:
		html += "<ul>\n"

	for i in obj.items:
		html += "<li>" + parToHtml(i.paragraph)[3:-5] + "</li>\n"
		html += rlistToHtml(i, ordered, level+1)

	if ordered:
		html += "</ol>\n"
	else:
		html += "</ul>\n"
	return html

def getType(level):
	if level == 0:
		return "type=\"1\""
	elif level == 1:
		return "type=\"a\""
	elif level == 2:
		return "type=\"i\""
	elif level == 3:
		return "type=\"A\""
	elif level == 4:
		return "type=\"I\""
	elif level > 4:
		return getType(level-5)
	else:
		return ""

def tableToHtml(obj):
	cols = len(obj.table)
	rows = len(obj.table[0])
	html = "<table>\n"

	html += "<tr>\n"
	for i in range(0, cols):
		html += "<th>" + obj.table[i][1] + "</th>\n"
	html += "<tr>\n"

	for j in range(2, rows):
		html += "<tr>\n"
		for i in range(0, cols):
			html += "<td style=\"text-align: " + obj.table[i][0] + "\">"
			html += obj.table[i][j]
			html += "</td>\n"
		html += "</tr>\n"
	
	html += "</table>\n"
	return html

def codeBlockToHtml(obj):
	html = "<div class=\"codeBlock\">\n"
	for line in obj.lines:
		newText = line
		newText = str.replace(newText, "\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
		newText = str.replace(newText, "<", "&lt;")
		newText = str.replace(newText, ">", "&gt;")
		html += newText
		html += "\n<br>\n"
	html += "</div>\n"
	return html

