#!/usr/bin/env python3

#Parses the markdown string into a list of line tokens.
#Each token contains the line string and a type.
#Possible types are: List, Divider, Header, Image,
#Code Block, Table, Text

#Token class
#Contains the line string and it's type.
class Token:
	def __init__(self, line, type):
		self.line = line
		self.type = type

	def __repr__(self):
		return self.type

#List Token Class
#Token class with added field for tabs in list.
class ListToken:
	def __init__(self, line, tabs, type="List"):
		self.line = line
		self.tabs = tabs
		self.type = type

	def __repr__(self):
		return self.type

#returns the list of tokens
#md is the markdown string to parse
def tokenize(md):
	tokens = []
	for line in md.splitlines():
		if line == "":
			tokens.append(Token(line, "Divider"))
		elif line[0] == "#":
			tokens.append(Token(line, "Header"))
		elif line[0] == "!":
			tokens.append(Token(line, "Image"))
		elif isList(line):
			tabs = countTabs(line)
			tokens.append(ListToken(line, tabs))
		elif line[:3] == "```":
			tokens.append(Token(line, "Code Block"))
		elif " | " in line:
			tokens.append(Token(line, "Table"))		
		else:
			tokens.append(Token(line, "Text"))		
	return tokens

#returns the first nonwhitespace character
#str is the string to search
def getFirstNWS(str):
	for c in str:
		if c != "\t" and c != " " and c != "\n":
			return c

#returns the number of tabs in the given string
#str is the string to search
def countTabs(str):
	count = 0
	for c in str:
		if c == "\t":
			count = count + 1
		else:
			break
	return count

#returns true if a line is part of a list, false otherwise
#line is the line to check
def isList(line):
	for i in range(0, len(line)):
		if line[i] == "*":
			if line[i+1] == " ":
				return True
		elif line[i].isdigit():
			if line[i+1:i+3] == ". ":
				return True
		elif line[i] == "\t":
			continue
		else:
			return False
