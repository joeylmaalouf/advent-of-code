#!/usr/bin/python3
import math


def main (filepath):
	instructions = parse_input(filepath)
	print('part 1:', count_tail_positions(instructions, 2))
	print('part 2:', count_tail_positions(instructions, 10))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of direction-distance pairs
		directions = {
			'U': (-1, 0),
			'D': (1, 0),
			'L': (0, -1),
			'R': (0, 1),
		}
		return [
			(directions[line.split()[0]], int(line.split()[1]))
			for line in filehandle.read().strip().split('\n')
		]


def count_tail_positions (instructions, num_knots):
	# we can move the head according to the instructions to see where the tail goes
	unique_tail_pos = set()
	knots = [[0, 0] for _ in range(num_knots)]
	for (direction, distance) in instructions:
		for _ in range(distance):
			knots[0][0] += direction[0]
			knots[0][1] += direction[1]
			for i in range(len(knots))[1 :]:
				knots[i] = move_tail(knots[i - 1], knots[i])
			unique_tail_pos.add(tuple(knots[-1]))
	return len(unique_tail_pos)


def move_tail (head_pos, tail_pos):
	# the tail tries to remain next to the head
	# it'll move in line if the head is in line, or diagonally if the head is shifted
	x_diff = head_pos[1] - tail_pos[1]
	y_diff = head_pos[0] - tail_pos[0]
	x_dist = int(math.copysign(1, x_diff))
	y_dist = int(math.copysign(1, y_diff))
	if x_diff < -1 or 1 < x_diff:
		tail_pos[1] += x_dist
		if y_diff != 0:
			tail_pos[0] += y_dist
	elif y_diff < -1 or 1 < y_diff:
		tail_pos[0] += y_dist
		if x_diff != 0:
			tail_pos[1] += x_dist
	return tail_pos


if __name__ == '__main__':
	main('input.txt')
