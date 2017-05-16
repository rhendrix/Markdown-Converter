#!/usr/bin/env python3

import sys
from mdcCollecter import *
from mdcConverter import *
from mdcTokenizer import *
from mdcClasses import *
from mdcHtml import *
from mdcLatex import *

#Main script
#Converts markdown into tokens, tokens into objects, and
#objects into either HTML or LaTeX.

#Takes 3 Arguments
#argv[1] is the file type, html or latex, to convert to.
#argv[2] is the input filename
#argv[3] is the output filename

if len(sys.argv) != 4:
	print("Usage: mdc type input output")
	sys.exit(0)
else:
	md = collect(sys.argv[2])
	tokens = tokenize(md)
	objects = tokensToObjects(tokens)
	if sys.argv[1] == "html":
		html = toHtml(objects)
		f = open(sys.argv[3], 'w')
		f.write(html)
		f.close()
	elif sys.argv[1] == "latex":
		latex = toLatex(objects)
		f = open(sys.argv[3], 'w')
		f.write(latex)
		f.close()
	else:
		print("Error: not a valid type")
		sys.exit(0)
