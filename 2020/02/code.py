#!/usr/bin/python

import re

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
entries = filehandle.read().strip().split('\n')
filehandle.close()

valid = 0
pattern = re.compile(r'(?P<n1>\d+)-(?P<n2>\d+) (?P<character>\w): (?P<password>\w+)')
for entry in entries:
	match = pattern.match(entry)
	password = match.group('password')
	character = match.group('character')
	if v2:
		if [password[int(match.group(key)) - 1] for key in ['n1', 'n2']].count(character) == 1:
			valid += 1
	else:
		count = password.count(character)
		if int(match.group('n1')) <= count <= int(match.group('n2')):
			valid += 1
print valid
