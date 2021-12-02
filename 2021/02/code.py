#!/usr/bin/python3


def main (filepath):
	commands = parse_input(filepath)
	print('part 1:', get_position(commands, False))
	print('part 2:', get_position(commands, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of direction-amount pairs
		commands = filehandle.read().strip().split('\n')
		for index in range(len(commands)):
			direction, amount = commands[index].split(' ')
			commands[index] = (direction[0], int(amount))
		return commands


def get_position (commands, complex_instr):
	horizontal = 0
	vertical = 0
	aim = 0

	# these functions represent the different ways we change our horizontal (x), vertical (y), and aim (a) values by some amount (n)
	if not complex_instr:
		instruction_fns = {
			'f': lambda x, y, a, n: (x + n, y, a),
			'd': lambda x, y, a, n: (x, y + n, a),
			'u': lambda x, y, a, n: (x, y - n, a),
		}
	else:
		instruction_fns = {
			'f': lambda x, y, a, n: (x + n, y + n * a, a),
			'd': lambda x, y, a, n: (x, y, a + n),
			'u': lambda x, y, a, n: (x, y, a - n),
		}

	for direction, amount in commands:
		horizontal, vertical, aim = instruction_fns[direction](horizontal, vertical, aim, amount)

	return horizontal * vertical


if __name__ == '__main__':
	main('input.txt')
