#!/usr/bin/python3


def main (filepath):
	depths = parse(filepath)
	print('part 1:', increases(depths, 0)) # a 0-wide window on either side means 1 data point alone
	print('part 2:', increases(depths, 1)) # a 1-wide window on either side means 3 data points combined


def parse (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers
		return [int(depth) for depth in filehandle.read().strip().split('\n')]


def increases (depths, window):
	count = 0

	# the first entry should always be skipped, since we have no prior value to compare against
	# we should also do the same for the first and last entries up to the window size so that we don't get any partial sums
	for index in range(len(depths))[(1 + window) : (len(depths) - window)]:
		current = sum(depths[(index - window) : (index + 1 + window)])
		previous = sum(depths[(index - 1 - window) : (index + window)])
		if current > previous:
			count += 1

	return count


if __name__ == '__main__':
	main('input.txt')
