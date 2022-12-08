#!/usr/bin/python3


def main (filepath):
	tree_heights = parse_input(filepath)
	visible_count, most_scenic = total_visibility(tree_heights)
	print('part 1:', visible_count)
	print('part 2:', most_scenic)


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a 2D array of numbers
		return [
			[int(n) for n in line]
			for line in filehandle.read().strip().split('\n')
		]


def total_visibility (tree_heights):
	# we want to find how many trees are visible from any edge of the forest in any cardinal direction
	visible_count = 0
	directions = (
		(-1, 0),
		(1, 0),
		(0, -1),
		(0, 1),
	)
	# and we want to keep track of the highest scenic score
	most_scenic = 0
	for y in range(len(tree_heights)):
		for x in range(len(tree_heights[0])):
			visible_anywhere = False
			scenic_score = 1
			for direction in directions:
				viewing_distance, visible_from_edge = directional_visibility(tree_heights, x, y, direction)
				if visible_from_edge:
					visible_anywhere = True
				scenic_score *= viewing_distance
			if visible_anywhere:
				visible_count += 1
			most_scenic = max(most_scenic, scenic_score)
	return visible_count, most_scenic


def directional_visibility (tree_heights, x, y, direction):
	# we'll check how far the sight line from the tree at the given coords can go in the given direction until it's blocked
	tree_height = tree_heights[y][x]
	x += direction[0]
	y += direction[1]
	blocked = False
	viewing_distance = 0
	while 0 <= x and x < len(tree_heights[0]) and 0 <= y and y < len(tree_heights):
		if not blocked:
			viewing_distance += 1
		if tree_heights[y][x] >= tree_height:
			blocked = True
		x += direction[0]
		y += direction[1]
	return viewing_distance, not blocked


if __name__ == '__main__':
	main('input.txt')
