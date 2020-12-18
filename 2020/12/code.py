#!/usr/bin/python

from math import radians, sin, cos

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
instructions = filehandle.read().strip().split('\n')
filehandle.close()

ship = [0, 0]
directions = {
	0: (0, -1),
	90: (1, 0),
	180: (0, 1),
	270: (-1, 0)
}
headings = {
	'N': 0,
	'E': 90,
	'S': 180,
	'W': 270,
	'F': 90
}
rotations = {
	'L': -1,
	'R': 1
}

if v2:
	waypoint = [10, -1]
	for instruction in instructions:
		action, value = instruction[0], int(instruction[1:])
		if action == 'F':
			for i in range(0, len(ship)):
				ship[i] += waypoint[i] * value
		elif action in headings.keys():
			displacement = directions[headings[action]]
			for i in range(0, len(waypoint)):
				waypoint[i] += displacement[i] * value
		elif action in rotations.keys():
			rotation = rotations[action] * value
			headings['F'] = (headings['F'] + rotation) % 360
			s = sin(radians(rotation))
			c = cos(radians(rotation))
			newx = int(round(waypoint[0] * c - waypoint[1] * s))
			newy = int(round(waypoint[0] * s + waypoint[1] * c))
			waypoint = [newx, newy]
else:
	for instruction in instructions:
		action, value = instruction[0], int(instruction[1:])
		if action in rotations.keys():
			headings['F'] = (headings['F'] + rotations[action] * value) % 360
		elif action in headings.keys():
			displacement = directions[headings[action]]
			for i in range(0, len(ship)):
				ship[i] += displacement[i] * value
print sum([abs(n) for n in ship])
