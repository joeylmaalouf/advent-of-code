#!/usr/bin/python3


def main (filepath):
	lines = parse_input(filepath)
	print('part 1:', count_overlaps(lines, False))
	print('part 2:', count_overlaps(lines, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of pairs of coordinate pairs
		return [
			[
				[
					int(value) for value in pair.split(',')
				] for pair in line.split(' -> ')
			] for line in filehandle.read().strip().split('\n')
		]


def count_overlaps (lines, include_diagonals):
	# rather than making an actual 2D representation, it's more efficient to just store a mapping of marked points to how many lines cover them
	points = {}
	for line in lines:
		for point in get_points(line, include_diagonals):
			key = tuple(point)
			points[key] = points.get(key, 0) + 1
	# we're only interested in how many points have overlapping lines on them, so we'll just count the ones with more than 1 line
	return len([n for n in points.values() if n > 1])


def get_points (line, include_diagonals):
	# we only want to return any points if the line is vertical or horizontal, or if we explicitly want to include diagonals
	if line[0][0] == line[1][0] or line[0][1] == line[1][1] or include_diagonals:
		x_range = get_range(line[0][0], line[1][0])
		y_range = get_range(line[0][1], line[1][1])
		# if the line is vertical or horizontal, we need to duplicate that one matching coordinate enough times to pair with the changing one
		if len(x_range) == 1:
			x_range *= len(y_range)
		if len(y_range) == 1:
			y_range *= len(x_range)
		return zip(x_range, y_range)
	else:
		return []


def get_range (val1, val2):
	# adding the step to the end of the range makes it inclusive, since it's exclusive by default
	step = 1 if val1 <= val2 else -1
	return list(range(val1, val2 + step, step))


if __name__ == '__main__':
	main('input.txt')
