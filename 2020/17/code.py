#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
initial = filehandle.read().strip()
filehandle.close()

grid = {}
for w, hypercube in enumerate([[initial.split('\n')]]):
	grid[w] = {}
	for z, layer in enumerate(hypercube):
		grid[w][z] = {}
		for y, row in enumerate(layer):
			grid[w][z][y] = {}
			for x, cube in enumerate(row):
				grid[w][z][y][x] = cube

def run_cycle(grid):
	newgrid = {}
	for w in (range(min(grid) - 1, max(grid) + 2) if v2 else [0]):
		newgrid[w] = {}
		if w not in grid:
			grid[w] = {}
		for z in range(min(grid[0]) - 1, max(grid[0]) + 2):
			newgrid[w][z] = {}
			if z not in grid[w]:
				grid[w][z] = {}
			for y in range(min(grid[0][0]) - 1, max(grid[0][0]) + 2):
				newgrid[w][z][y] = {}
				if y not in grid[w][z]:
					grid[w][z][y] = {}
				for x in range(min(grid[0][0][0]) - 1, max(grid[0][0][0]) + 2):
					if x not in grid[w][z][y]:
						grid[w][z][y][x] = '.'
					neighbors = count_active_neighbors(grid, w, z, y, x)
					if grid[w][z][y][x] == '#' and neighbors in (2, 3):
						newgrid[w][z][y][x] = '#'
					elif grid[w][z][y][x] == '.' and neighbors == 3:
						newgrid[w][z][y][x] = '#'
					else:
						newgrid[w][z][y][x] = '.'
	return newgrid

def count_active_neighbors(grid, w, z, y, x):
	active = 0
	neighbors = get_neighbors(w, z, y, x)
	for (nw, nz, ny, nx) in neighbors:
		if nw in grid and nz in grid[nw] and ny in grid[nw][nz] and nx in grid[nw][nz][ny] and grid[nw][nz][ny][nx] == '#':
			active += 1
	return active

def get_neighbors(w, z, y, x):
	neighbors = []
	for nw in (range(w - 1, w + 2) if v2 else [w]):
		for nz in range(z - 1, z + 2):
			for ny in range(y - 1, y + 2):
				for nx in range(x - 1, x + 2):
					if not (nw == w and nz == z and ny == y and nx == x):
						neighbors.append((nw, nz, ny, nx))
	return neighbors

for _ in range(6):
	grid = run_cycle(grid)
print ''.join(
	''.join(
		''.join(
			''.join(
				row.values()
			) for row in layer.values()
		) for layer in hypercube.values()
	) for hypercube in grid.values()
).count('#')
