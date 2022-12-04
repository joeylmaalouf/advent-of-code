#!/usr/bin/python3


def main (filepath):
	calorie_groups = parse_input(filepath)
	print('part 1:', max_groups(calorie_groups, 1))
	print('part 2:', max_groups(calorie_groups, 3))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers separated into groups via an extra newline
		# we'll split by double newline to get the groups, then in each group split by newline and convert to number to get the individual values
		return [
			[
				int(calories)
				for calories in group.split('\n')
			]
			for group in filehandle.read().strip().split('\n\n')
		]


def max_groups (calorie_groups, count):
	# we sum the group calorie totals, sort them from largest to smallest, and sum however many totals we require
	return sum(
		sorted(
			(sum(group) for group in calorie_groups),
			reverse = True
		)[0 : count]
	)


if __name__ == '__main__':
	main('input.txt')
