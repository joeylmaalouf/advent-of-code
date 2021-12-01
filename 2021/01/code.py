#!/usr/bin/python3


def main (filepath):
	# the input is a list of numbers
	filehandle = open(filepath, 'r')
	depths = [int(depth) for depth in filehandle.read().strip().split('\n')]
	filehandle.close()

	print('part 1:', get_increases(depths, 0)) # a 0-wide window on either side means 1 data point alone
	print('part 2:', get_increases(depths, 1)) # a 1-wide window on either side means 3 data points combined


def get_increases (values, window):
	increases = 0
	# the first entry should always be skipped, since we have no prior value to compare against
	# we should also do the same for the first and last entries up to the window size so that we don't get any partial sums
	for index in range(len(values))[(1 + window) : (len(values) - window)]:
		current = sum(values[(index - window) : (index + 1 + window)])
		previous = sum(values[(index - 1 - window) : (index + window)])
		if current > previous:
			increases += 1
	return increases


if __name__ == '__main__':
	main('input.txt')
