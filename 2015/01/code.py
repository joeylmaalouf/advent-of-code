#!/usr/bin/python3


def main (filepath):
	instructions = parse_input(filepath)
	print('part 1:', instructions.count('(') - instructions.count(')'))
	print('part 2:', find_basement(instructions))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return filehandle.read().strip()


def find_basement (instructions):
	level = 0
	for i, instr in enumerate(instructions):
		level += {'(' : 1, ')' : -1}[instr]
		if level < 0:
			return i + 1


if __name__ == '__main__':
	main('input.txt')
