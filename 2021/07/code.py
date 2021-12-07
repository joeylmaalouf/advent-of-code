#!/usr/bin/python3


def main (filepath):
	positions = parse_input(filepath)
	print('part 1:', minimize_fuel(positions, simple_cost))
	print('part 2:', minimize_fuel(positions, complex_cost))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers
		return [int(value) for value in filehandle.read().strip().split(',')]


def minimize_fuel (positions, cost_fn):
	# we want the minimum total fuel usage for all the submarines, and we'll check potential options anywhere within the current range of positions
	return min(
		sum(
			cost_fn(position, option)
			for position in positions
		)
		for option in range(min(positions), max(positions) + 1)
	)


def simple_cost (old, new):
	# 1 fuel per unit traveled
	return abs(old - new)


def complex_cost (old, new):
	# 1 fuel for the first unit traveled, 2 for the second, 3 for the third, etc.
	# return sum(range(simple_cost(old, new) + 1))
	# the above code isn't too inefficient, but wikipedia gives a nice formula for 1 + 2 ... + n
	n = simple_cost(old, new)
	return int((n * (n + 1)) / 2)


if __name__ == '__main__':
	main('input.txt')
