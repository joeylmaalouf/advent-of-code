#!/usr/bin/python3


def main (filepath):
	range_pairs = parse_input(filepath)
	print('part 1:', count_overlapping_pairs(range_pairs, True))
	print('part 2:', count_overlapping_pairs(range_pairs, False))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of pairs of number ranges
		return [
			[
				[
					int(n)
					for n in ranges.split('-')
				]
				for ranges in pair.split(',')
			]
			for pair in filehandle.read().strip().split('\n')
		]


def count_overlapping_pairs (range_pairs, need_all):
	# we want to increase our counter when we find that one of the ranges in each range pair overlaps the other,
	# but sometimes we want to check if all of the values are present (subset) and sometimes we just want to check if any of the values are
	count = 0
	for range_pair in range_pairs:
		range1, range2 = (set(range(range_ends[0], range_ends[1] + 1)) for range_ends in range_pair)
		if need_all and (range1.issubset(range2) or range2.issubset(range1)):
			count += 1
		if not need_all and not range1.isdisjoint(range2):
			count += 1
	return count


if __name__ == '__main__':
	main('input.txt')
