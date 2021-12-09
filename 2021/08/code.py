#!/usr/bin/python3


def main (filepath):
	entries = parse_input(filepath)
	print('part 1:', unique_digits(entries))
	print('part 2:', sum_outputs(entries))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of entries that are made up of signal patterns and output values
		entries = [
			line.split(' | ')
			for line in filehandle.read().strip().split('\n')
		]
		return [
			(entry[0].split(), entry[1].split())
			for entry in entries
		]


def unique_digits(entries):
	# we want to count how many times just the uniquely identifiable lengths appeared
	# in a standard 7-segment display, the digits represented by a unique number of segments are 1, 4, 7, and 8 (with counts of 2, 4, 3, and 7 respectively)
	lengths = [2, 4, 3, 7]
	return sum([
		sum([
			1 if len(value) in lengths else 0
			for value in values
		])
		for _, values in entries
	])


def sum_outputs (entries):
	return sum(
		decode(patterns, values)
		for patterns, values in entries
	)


def decode (patterns, values):
	# the order of segments within a set doesn't matter, so let's sort them for ease of comparison
	patterns = [sorted(pattern) for pattern in patterns]
	values = [sorted(value) for value in values]

	mapping = {}
	# if we see any digits that are uniquely identifiable by their segment count, we can note their mapping first
	unique_lengths = {
		1: 2,
		4: 4,
		7: 3,
		8: 7,
	}
	for digit, length in unique_lengths.items():
		for pattern in patterns:
			if len(pattern) == length:
				mapping[digit] = pattern
				break

	# the rest of the digits are only partially identifiable by their segment count, but now that we know the signals for 1, 4, 7, and 8,
	# we can figure out which sets of signals correspond to each of the other digits by looking at how many segments they share with the ones we do know
	# huge thanks to the adventofcode subreddit for hint to think about what segments the numbers share
	for pattern in patterns:
		if len(pattern) == 5:
			# 2 is the only digit whose display has 5 segments and also shares exactly 2 of them with 4's display
			if len(intersection(pattern, mapping[4])) == 2:
				mapping[2] = pattern
			# 3 is the only digit whose display has 5 segments and also shares exactly 2 of them with 1's display
			elif len(intersection(pattern, mapping[1])) == 2:
				mapping[3] = pattern
			# 5 is the only digit whose display has 5 segments besides 2 and 3, handled above
			else:
				mapping[5] = pattern
		elif len(pattern) == 6:
			# 6 is the only digit whose display has 6 segments and also shares exactly 1 of them with 1's display
			if len(intersection(pattern, mapping[1])) == 1:
				mapping[6] = pattern
			# 9 is the only digit whose display has 6 segments and also shares exactly 4 of them with 4's display
			elif len(intersection(pattern, mapping[4])) == 4:
				mapping[9] = pattern
			# 0 is the only digit whose display has 6 segments besides 6 and 9, handled above
			else:
				mapping[0] = pattern

	# we'll need to invert our mapping to make it useful for decoding
	mapping = {''.join(segments): digit for digit, segments in mapping.items()}
	# then we can check each digit value against the mapping and join the decoded digits into an actual number
	return int(''.join([
		str(mapping[''.join(value)])
		for value in values
	]))


def intersection (a, b):
	return [c for c in a if c in b]


if __name__ == '__main__':
	main('input.txt')
