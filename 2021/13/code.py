#!/usr/bin/python3


def main (filepath):
	dots, folds = parse_input(filepath)
	print('part 1:', count_folded_dots(dots, folds[:1]))
	print('part 2:', visualize_folded_dots(dots, folds))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a series of coordinate pairs followed by a series of fold instructions
		dots, folds = filehandle.read().strip().split('\n\n')
		dots = [
			[int(coordinate) for coordinate in pair.split(',')]
			for pair in dots.split('\n')
		]
		folds = [
			fold.replace('fold along ', '').split('=')
			for fold in folds.split('\n')
		]
		for fold in folds:
			fold[1] = int(fold[1])
		return dots, folds


def count_folded_dots (dots, folds):
	dots = get_folded_dots(dots, folds)
	# to get the number of unique dots, we'll stringify the coordinates so that we can turn the list into a set
	return len(set(
		','.join(
			str(coordinate)
			for coordinate in dot
		) for dot in dots
	))


def get_folded_dots (dots, folds):
	for direction, line in folds:
		index = {'x': 0, 'y': 1}[direction]
		for dot in dots:
			# any dots over the line need their position updated to account for the folding
			if dot[index] > line:
				dot[index] = 2 * line - dot[index]
	return dots


def visualize_folded_dots (dots, folds):
	dots = get_folded_dots(dots, folds)
	# we can visualize the dots by plotting them as joined strings
	max_x = max(dot[0] for dot in dots)
	max_y = max(dot[1] for dot in dots)
	rows = []
	for y in range(max_y + 1):
		row = []
		for x in range(max_x + 1):
			row.append('█' if [x, y] in dots else ' ')
		rows.append(''.join(row))
	return '\n' + '\n'.join(rows)


if __name__ == '__main__':
	main('input.txt')
