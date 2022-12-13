#!/usr/bin/python3
import functools


def main (filepath):
	pairs = parse_input(filepath)
	print('part 1:', sum(correct_order_indices(pairs)))
	print('part 2:', get_decoder_key(pairs, [[[2]], [[6]]]))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of paired lines that we can evaluate to turn into proper lists
		# this would be dangerous if we didn't trust our input
		return [
			[
				eval(line)
				for line in pair.split('\n')
			]
			for pair in filehandle.read().strip().split('\n\n')
		]


def correct_order_indices (pairs):
	indices = []
	for i in range(len(pairs)):
		if in_correct_order(*pairs[i]):
			indices.append(i + 1)
	return indices


def in_correct_order (left, right):
	if isinstance(left, int) and isinstance(right, int):
		# if both values are numbers, the left one should be lower to have the correct order
		# if they're the same, we move on to the next comparison
		if left == right:
			return None
		else:
			return left < right
	else:
		# if we don't have just ints, then we'll be comparing lists
		# first, we'll convert any ints to lists
		if isinstance(left, int): left = [left]
		if isinstance(right, int): right = [right]
		# now that we both values as lists, we can compare their elements
		for i in range(max(len(left), len(right))):
			if i >= len(left):
				# if the left list runs out first, it's in the correct order
				return True
			elif i >= len(right):
				# if the right list runs out first, it's not in the correct order
				return False
			else:
				# if we have elements in both lists, we can compare them recursively
				correct_order = in_correct_order(left[i], right[i])
				if correct_order is not None:
					return correct_order


def sort_fn (a, b):
	return {
		True: -1,
		None: 0,
		False: 1,
	}[in_correct_order(a, b)]


def get_decoder_key (pairs, dividers):
	# the full packet list is the given dividers plus every member of every pair
	packets = dividers[:]
	for pair in pairs:
		packets.extend(pair)
	packets.sort(key = functools.cmp_to_key(sort_fn))
	# after sorting all of the packets, we want to get the divider indices and turn them into the decoder key
	decoder_key = 1
	for divider in dividers:
		decoder_key *= packets.index(divider) + 1
	return decoder_key


if __name__ == '__main__':
	main('input.txt')
