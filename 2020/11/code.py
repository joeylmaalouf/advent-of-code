#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
seats = [list(line) for line in filehandle.read().strip().split('\n')]
filehandle.close()

def count_adjacent(seats, row, col):
	height, width = len(seats), len(seats[0])
	top, bot = row == 0, row == (height - 1)
	left, right = col == 0, col == (width - 1)
	adjacents = []
	for xbool, x in zip((left, False, right), (col - 1, col, col + 1)):
		for ybool, y in zip((top, False, bot), (row - 1, row, row + 1)):
			if not xbool and not ybool and not (x == col and y == row):
				adjacents.append((y, x))
	return len([1 for (y, x) in adjacents if seats[y][x] == '#'])

def count_visible(seats, row, col):
	height, width = len(seats), len(seats[0])
	top, bot = row == 0, row == (height - 1)
	left, right = col == 0, col == (width - 1)
	visible = []
	for xbool, dx in zip((left, False, right), (-1, 0, 1)):
		for ybool, dy in zip((top, False, bot), (-1, 0, 1)):
			if not xbool and not ybool and not (dx == 0 and dy == 0):
				y, x = row + dy, col + dx
				while (0 <= y < height) and (0 <= x < width):
					if seats[y][x] != '.':
						visible.append((y, x))
						break
					x += dx
					y += dy
	return len([1 for (y, x) in visible if seats[y][x] == '#'])

countfn = count_visible if v2 else count_adjacent
tolerance = 5 if v2 else 4
while True:
	newseats = [line[:] for line in seats]
	for row in range(0, len(newseats)):
		for col in range(0, len(newseats[row])):
			if newseats[row][col] != '.':
				occupied = countfn(seats, row, col)
				if newseats[row][col] == 'L' and occupied == 0:
					newseats[row][col] = '#'
				elif newseats[row][col] == '#' and occupied >= tolerance:
					newseats[row][col] = 'L'
	if newseats == seats:
		print ''.join([''.join(line) for line in seats]).count('#')
		break
	seats = newseats
