#!/usr/bin/env python3

import re

#Collects all of the markdown files referenced in the
#input file into a single string.

#returns the string containing the markdown to be converted
#filepath is the realtive path to the input file.
def collect(filePath):
	f = open(filePath, 'r')
	md = f.read()
	f.close()
	
	while True:
		imp = re.search("%\(.+\)", md)
		if imp == None:
			break
		line = md[imp.start():imp.end()]
		filePath = line[2:-1]
		f = open(filePath, 'r')
		new = f.read()
		f.close()
		md = str.replace(md, line, new)

	return md
