#!/usr/bin/python3


def main (filepath):
	rocks, sand_source = parse_input(filepath)
	print('part 1:', count_resting_sand(rocks, sand_source, False))
	print('part 2:', count_resting_sand(rocks, sand_source, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		rocks = set()
		# the input is a list of paths of points
		for structure in [
			[
				[
					int(n)
					for n in point.split(',')
				]
				for point in path.split(' -> ')
			]
			for path in filehandle.read().strip().split('\n')
		]:
			for i in range(1, len(structure)):
				start, end = structure[i - 1 : i + 1]
				if start[0] == end[0]:
					for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
						rocks.add((start[0], y))
				elif start[1] == end[1]:
					for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
						rocks.add((x, start[1]))
		return rocks, (500, 0)


def count_resting_sand (rocks, sand_source, with_floor):
	# we keep adding sand until it starts falling into the abyss or until it comes to rest over the source
	# then we can count how many units landed at rest
	resting_sand = set()
	falling_into_abyss = False
	draw_cave(rocks, sand_source, resting_sand, with_floor)
	while not (falling_into_abyss or sand_source in resting_sand):
		falling_into_abyss = add_sand(rocks, sand_source, resting_sand, with_floor)
	draw_cave(rocks, sand_source, resting_sand, with_floor)
	return len(resting_sand)


def add_sand (rocks, sand_source, resting_sand, with_floor):
	# the new unit of sand spawns at the source
	new_sand = list(sand_source)
	# we can keep taking a step until the sand comes to rest or falls into the abyss
	at_rest, in_abyss = False, False
	while not (at_rest or in_abyss):
		new_sand, at_rest, in_abyss = take_step(new_sand, rocks, resting_sand, with_floor)
	if at_rest:
		resting_sand.add(tuple(new_sand))
	return in_abyss


def take_step (new_sand, rocks, resting_sand, with_floor):
	# sand will fall straight down if possible, otherwise down left, otherwise down right
	# otherwise it comes to rest
	obstacles = rocks.union(resting_sand)
	at_rest = False
	below = (new_sand[0], new_sand[1] + 1)
	below_left = (new_sand[0] - 1, new_sand[1] + 1)
	below_right = (new_sand[0] + 1, new_sand[1] + 1)
	if below not in obstacles:
		new_sand = list(below)
	elif below_left not in obstacles:
		new_sand = list(below_left)
	elif below_right not in obstacles:
		new_sand = list(below_right)
	else:
		at_rest = True
	# if the sand has fallen past all rocks, then it's in the abyss
	in_abyss = new_sand[1] > max(y for _, y in rocks)
	# unless we have a floor
	if with_floor:
		if in_abyss:
			at_rest = True
			in_abyss = False
	return new_sand, at_rest, in_abyss


def draw_cave (rocks, sand_source, resting_sand, with_floor):
	# helpful for visualizing the state of things
	min_x = min(x for (x, _) in rocks.union(resting_sand)) - 1
	min_y = 0
	max_x = max(x for (x, _) in rocks.union(resting_sand)) + 1
	max_y = max(y for (_, y) in rocks) + 1
	if with_floor:
		max_y += 1
	for y in range(min_y, max_y + 1):
		line = ''
		for x in range(min_x, max_x + 1):
			line += \
				'#' if (x, y) in rocks else \
				'o' if resting_sand and (x, y) in resting_sand else \
				'+' if (x, y) == sand_source else \
				'.'
		if with_floor and y == max_y:
			line = '#' * (max_x - min_x + 1)
		print(line)


if __name__ == '__main__':
	main('input.txt')
