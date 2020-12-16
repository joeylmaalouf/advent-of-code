#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
boardingpasses = filehandle.read().strip().split('\n')
filehandle.close()

seatids = [
	int(boardingpass[0:7].replace('F', '0').replace('B', '1'), 2) * 8
		+ int(boardingpass[7:].replace('L', '0').replace('R', '1'), 2)
	for boardingpass in boardingpasses
]

if v2:
	print list(set(range(min(seatids), max(seatids) + 1)) - set(seatids))[0]
else:
	print max(seatids)
