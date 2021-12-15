#!/usr/bin/python3


def main (filepath):
	template, rules = parse_input(filepath)
	print('part 1:', get_frequency_difference(template, rules, 10))
	print('part 2:', get_frequency_difference(template, rules, 40))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a line of characters followed by a series of character mappings
		template, mappings = filehandle.read().strip().split('\n\n')
		rules = {}
		for rule in mappings.split('\n'):
			pair = rule.split(' -> ')
			rules[pair[0]] = pair[1]
		return list(template), rules


def get_frequency_difference (polymer, element_rules, steps):
	# we'll first want to create trackers for how many times each element and each pair appear in the polymer
	element_counts = {char: polymer.count(char) for char in set(polymer)}
	pair_counts = {}
	for index in range(len(polymer) - 1):
		pair = ''.join(polymer[index : index + 2])
		pair_counts[pair] = pair_counts.get(pair, 0) + 1

	# it's inefficient to actually build up the massive polymer over many iterations
	# but that's fine, we're only interested in the element counts, not the resulting string itself
	# so we can just build a mapping of what pairs are created from each pair's rule and work from that
	pair_rules = {
		pair: [pair[0] + element, element + pair[1]]
		for pair, element in element_rules.items()
	}

	for _ in range(steps):
		# we don't want to live update the counters that could be used in later calculations within the same step,
		# so we'll create, modify, and reassign cloned mappings in each step
		new_element_counts = {element: element_count for element, element_count in element_counts.items()}
		new_pair_counts = {pair: pair_count for pair, pair_count in pair_counts.items()}
		for pair, pair_count in pair_counts.items():
			if pair_count > 0:
				# first, we'll track the newly added elements themselves
				new_element = element_rules[pair]
				new_element_counts[new_element] = new_element_counts.get(new_element, 0) + pair_count
				# then, we'll remove from consideration the pair that has been broken up by the new element
				new_pair_counts[pair] -= pair_count
				# finally, we'll track the newly added pairs formed as a result of the new element
				for new_pair in pair_rules[pair]:
					new_pair_counts[new_pair] = new_pair_counts.get(new_pair, 0) + pair_count
		element_counts = new_element_counts
		pair_counts = new_pair_counts

	# the frequency difference is the difference between occurrences of the most and least frequent elements
	return max(element_counts.values()) - min(element_counts.values())


if __name__ == '__main__':
	main('input.txt')
