#!/usr/bin/env python3

latexHead = """\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{grffile}
\\usepackage{listings}
\\usepackage[hidelinks]{hyperref}
\\usepackage{ragged2e}
\\usepackage{color}
\\usepackage{courier}
\\usepackage{csquotes}

\\lstset{
	basicstyle=\\ttfamily,
	commentstyle=\\color{purple},
	keywordstyle=\\color{blue},
	identifierstyle=\\color{black},
	stringstyle=\\color{red},
	breaklines=true,
	frame=single
}

\setlength{\parskip}{0.5em}
\setlength{\parindent}{0pt}
"""

def toLatex(objects):
	latex = ""
	latex += latexHead
	latex += "\\begin{document}\n"
	for o in objects:
		if o.type == "Header":
			latex += headerToLatex(o)
		elif o.type == "Image":
			latex += imageToLatex(o)
		elif o.type == "Paragraph":
			latex += parToLatex(o)
		elif o.type == "List":
			latex += listToLatex(o)
		elif o.type == "Table":
			latex += tableToLatex(o)
		elif o.type == "Code Block":
			latex += codeBlockToLatex(o)
	latex += "\\end{document}\n"
	return latex

def headerToLatex(obj):
	latex = "\\"
	latex += headerStr(int(obj.headerLevel))
	latex += "*{"
	latex += obj.text 
	latex += "}\n"
	return latex

def headerStr(lvl):
	if lvl == 1:
		return "section"
	elif lvl == 2:
		return "subsection"
	elif lvl == 3:
		return "subsubsection"
	elif lvl == 4:
		return "paragraph"
	elif lvl == 5:
		return "subparagraph"
	return ""

def imageToLatex(obj):
	scale = float(obj.scale[:-1])/100
	latex = "\\begin{center}\n"
	latex += "\\includegraphics[width="
	latex += str(scale)
	latex += "\\textwidth]{"
	latex += obj.url
	latex += "}\n\\end{center}\n"
	return latex

def linkToLatex(obj):
	latex = "\\href{" + obj.url + "}{" + obj.text + "}"
	return latex

def parToLatex(obj):
	latex = "\\par\n"
	for t in obj.textItems:
		if t.type == "Text":
			if t.bold:
				latex += "\\textbf{"
			if t.it:
				latex += "\\textit{"
			if t.code:
				latex += "{\\fontfamily{pcr}\\selectfont\\framebox[1.1\\width]{"

			newText = t.text
			newText = str.replace(newText, "<", "$<$")
			newText = str.replace(newText, ">", "$>$")
			latex += newText

			if t.code:
				latex += "}}"
			if t.it:
				latex += "}"
			if t.bold:
				latex += "}"
		elif t.type == "Link":
			latex += linkToLatex(t)
		latex += "\n"
	latex += "\n"
	return latex

def listToLatex(obj):
	return rlistToLatex(obj, obj.ordered, 0)

def rlistToLatex(obj, ordered, level):
	if len(obj.items) == 0:
		return ""
	latex = ""
	if ordered:
		latex += "\\begin{enumerate}\n"
	else:
		latex += "\\begin{itemize}\n"

	for i in obj.items:
		latex += "\\item " + parToLatex(i.paragraph)[5:-2] + "\n"
		latex += rlistToLatex(i, ordered, level+1)

	if ordered:
		latex += "\\end{enumerate}\n"
	else:
		latex += "\\end{itemize}\n"
	return latex

def tableToLatex(obj):
	cols = len(obj.table)
	rows = len(obj.table[0])
	latex = "\\begin{tabular}{ "

	for i in range(0, cols):
		latex += obj.table[i][0][0] + " "
	latex += "}\n"	

	head = ""
	for i in range(0, cols):
		head += "\\Centering\\textbf{" + obj.table[i][1] + "} & "
	latex += head[:-2] + "\\\\\n"

	latex += "\\hline\n"

	for j in range(2, rows):
		cell = ""
		for i in range(0, cols):
			cell += obj.table[i][j] + " & "
		latex += cell[:-2] + "\\\\\n"
	
	latex += "\end{tabular}\n"
	return latex

def codeBlockToLatex(obj):
	latex = "\\begin{lstlisting}[language=" + obj.lang + "]\n"
	for line in obj.lines:
		newText = line
		latex += newText + "\n"
	latex += "\\end{lstlisting}\n"
	return latex
