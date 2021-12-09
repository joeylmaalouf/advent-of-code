#!/usr/bin/python3


def main (filepath):
	heights = parse_input(filepath)
	print('part 1:', risk_sum(heights))
	print('part 2:', basin_product(heights, 3))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a 2D array of numbers
		return [
			[
				int(n)
				for n in line
			] for line in filehandle.read().strip().split('\n')
		]


def risk_sum (heights):
	# risk is just calculated as height + 1 for any height that is lower than all of its adjacent points
	return sum(
		height + 1
		for height in get_low(heights).values()
	)


def get_low (heights):
	low = {}
	for y in range(len(heights)):
		for x in range(len(heights[0])):
			if all(
				heights[y][x] < adjacent
				for adjacent in get_adjacent(heights, x, y).values()
			):
				low[tuple((x, y))] = heights[y][x]
	return low


def get_adjacent (heights, x, y):
	adjacent = {}
	# we have to account for array boundaries
	if y > 0:                   adjacent[tuple((x, y - 1))] = heights[y - 1][x]
	if y < len(heights) - 1:    adjacent[tuple((x, y + 1))] = heights[y + 1][x]
	if x > 0:                   adjacent[tuple((x - 1, y))] = heights[y][x - 1]
	if x < len(heights[0]) - 1: adjacent[tuple((x + 1, y))] = heights[y][x + 1]
	return adjacent


def basin_product (heights, count):
	basin_sizes = []
	for (x, y) in get_low(heights).keys():
		basin_sizes.append(len(get_basin(heights, x, y, {}).values()))

	product = 1
	for basin_size in sorted(basin_sizes, reverse = True)[:count]:
		product *= basin_size
	return product


def get_basin (heights, x, y, basin_points):
	basin_points[tuple((x, y))] = 1
	# to get the size of a basin, we can start at its low point and climb in every direction until we hit all 9s, tracking the unique points we covered on the way
	for position, height in get_adjacent(heights, x, y).items():
		if height != 9 and height > heights[y][x]:
			basin_points = get_basin(heights, position[0], position[1], basin_points)
	return basin_points


if __name__ == '__main__':
	main('input.txt')
