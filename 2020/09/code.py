#!/usr/bin/python

from itertools import combinations 

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
values = [int(n) for n in filehandle.read().strip().split('\n')]
filehandle.close()

window = 25

invalid = None
index = window
while index < len(values):
	if not any(
		sum(components) == values[index]
		for components in list(combinations(values[index - window:index], 2))
	):
		invalid = values[index]
		break
	index += 1

if v2:
	if invalid is not None:
		start = 0
		end = 2
		while start < len(values) - 2:
			while end < len(values) + 1:
				contiguous = values[start:end]
				if sum(contiguous) == invalid:
					print min(contiguous) + max(contiguous)
				end += 1
			start += 1
			end = start + 2
else:
	print invalid
