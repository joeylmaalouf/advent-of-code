#!/usr/bin/python3


def main (filepath):
	numbers, base = parse_input(filepath)
	print(base)
	print('part 1:', power_consumption(numbers, base))
	print('part 2:', lifesupport_rating(numbers, base))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers as digit strings
		numbers = filehandle.read().strip().split('\n')
		# if we assume that all valid characters show up somewhere in the input, then we can determine the base automatically (e.g. only 0s and 1s means it's binary)
		return numbers, len(set(''.join(numbers)))


def digit_counts (numbers, base):
	length = len(numbers[0])
	counts = [{n: 0 for n in range(base)} for _ in range(length)]

	# getting a mapping of each option's frequency in each digit will come in handy later
	for number in numbers:
		for index in range(length):
			counts[index][int(number[index])] += 1

	return counts


def power_consumption (numbers, base):
	counts = digit_counts(numbers, base)

	# the gamma and epsilon rates are just the joined strings of the most and least frequent digit values respectively
	gamma_rate = ''.join(str(max(count, key = lambda n: count[n])) for count in counts)
	epsilon_rate = ''.join(str(min(count, key = lambda n: count[n])) for count in counts)

	# then we just need to convert the digit strings to decimal
	return int(gamma_rate, base) * int(epsilon_rate, base)


def lifesupport_rating (numbers, base):
	counts = digit_counts(numbers, base)

	# the oxygen and co2 ratings are values in our list that most closely match our most and least frequent digits respectively
	oxygen_rating = filter_digits(numbers, base, counts, max, 1, 0)
	co2_rating = filter_digits(numbers, base, counts, min, 0, 0)

	# then we just need to convert the digit strings to decimal
	return int(oxygen_rating, base) * int(co2_rating, base)


def filter_digits (numbers, base, counts, filter, tie_winner, index):
	# desired digits are any that match our given filter func (e.g. max, min, etc.)
	filtered = filter(counts[index].values())
	matching = [key for key, value in counts[index].items() if value == filtered]
	# if there are multiple, we'll default to the given tie winner
	keep = matching[0] if len(matching) == 1 else tie_winner
	# and we only want to keep values that have the desired digit where we want it
	valid = [number for number in numbers if int(number[index]) == keep]
	if len(valid) == 0:
		# if we have no valid values left, then something went wrong and we'll just return 0
		return 0
	elif len(valid) == 1:
		# if we only have one valid value left, that's all we need
		return valid[0]
	else:
		# otherwise, we'll repeat this process on just the valid subset of data, checking the next digit over
		return filter_digits(valid, base, digit_counts(valid, base), filter, tie_winner, index + 1)


if __name__ == '__main__':
	main('input.txt')
