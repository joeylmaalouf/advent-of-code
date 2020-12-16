#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
grid = [list(line) for line in filehandle.read().strip().split('\n')]
filehandle.close()

def count_trees(grid, slope):
	height, width = len(grid), len(grid[0])
	position = [0, 0]
	trees = 0
	finished = False
	while not finished:
		if grid[position[1]][position[0]] == '#':
			trees += 1
		position[0] = (position[0] + slope[0]) % width
		position[1] += slope[1]
		if position[1] >= height:
			finished = True
	return trees

if v2:
	print count_trees(grid, (1, 1)) \
		* count_trees(grid, (3, 1)) \
		* count_trees(grid, (5, 1)) \
		* count_trees(grid, (7, 1)) \
		* count_trees(grid, (1, 2))
else:
	print count_trees(grid, (3, 1))
