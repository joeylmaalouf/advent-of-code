#!/usr/bin/python3


def main (filepath):
	boxes = parse_input(filepath)
	print('part 1:', sum(map(wrapping_paper, boxes)))
	print('part 2:', sum(map(ribbon, boxes)))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return [
			sorted([
				int(n)
				for n in box.split('x')
			])
			for box in filehandle.read().strip().split("\n")
		]


def wrapping_paper (box):
	return (2 * box[0] * box[1]) + (2 * box[0] * box[2]) + (2 * box[1] * box[2]) + (box[0] * box[1])


def ribbon (box):
	return (2 * box[0]) + (2 * box[1]) + (box[0] * box[1] * box[2])


if __name__ == '__main__':
	main('input.txt')
