#!/usr/bin/python3


def main (filepath):
	instructions = parse_input(filepath)
	print('part 1:', sum_lights(instructions, (1000, 1000), {
		'off': lambda n: 0,
		'on': lambda n: 1,
		'toggle': lambda n: 1 - n,
	}))
	print('part 2:', sum_lights(instructions, (1000, 1000), {
		'off': lambda n: max(n - 1, 0),
		'on': lambda n: n + 1,
		'toggle': lambda n: n + 2,
	}))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return [
			{
				'op': instruction.split('|')[0],
				'from': tuple(int(n) for n in instruction.split('|')[1].split(',')),
				'to': tuple(int(n) for n in instruction.split('|')[2].split(','))
			} for instruction in
			filehandle.read().strip().replace('turn ', '').replace('through ', '').replace(' ', '|').split('\n')
		]


def sum_lights (instructions, dimensions, operations):
	lights = [[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])]
	for instruction in instructions:
		for x in range(instruction['from'][0], instruction['to'][0] + 1):
			for y in range(instruction['from'][1], instruction['to'][1] + 1):
				lights[x][y] = operations[instruction['op']](lights[x][y])
	return sum(sum(l) for l in lights)


if __name__ == '__main__':
	main('input.txt')
