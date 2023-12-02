#!/usr/bin/python3


def main (filepath):
	directions = parse_input(filepath)
	print('part 1:', count_deliveries(directions, 1))
	print('part 2:', count_deliveries(directions, 2))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return filehandle.read().strip()


def count_deliveries (directions, num_santas):
	santas = [[0, 0] for _ in range(num_santas)]
	deliveries = {(0, 0): num_santas}
	santa_index = 0
	for direction in directions:
		current_santa = santas[santa_index]
		if direction == '<': current_santa[0] -= 1
		elif direction == '>': current_santa[0] += 1
		elif direction == '^': current_santa[1] -= 1
		elif direction == 'v': current_santa[1] += 1
		santas[santa_index] = current_santa[:]
		deliveries[tuple(current_santa)] = deliveries.get(tuple(current_santa), 0) + 1
		santa_index = (santa_index + 1) % num_santas
	return len(deliveries)


if __name__ == '__main__':
	main('input.txt')
