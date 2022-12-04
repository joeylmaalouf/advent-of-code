#!/usr/bin/python3


def main (filepath):
	item_lists = parse_input(filepath)
	print('part 1:', sum_mistake_priorities(item_lists))
	print('part 2:', sum_badge_priorities(item_lists))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of character sets
		return [
			list(rucksack)
			for rucksack in filehandle.read().strip().split('\n')
		]


def sum_mistake_priorities (item_lists):
	# first we need to find which items show up in both compartments (the first half and the second half of each list)
	# then we can get the sum of those mistaken items' priorities
	return sum(
		get_priority(find_shared([
			item_list[:len(item_list) // 2],
			item_list[len(item_list) // 2:]
		]))
		for item_list in item_lists
	)


def sum_badge_priorities (item_lists, group_size = 3):
	# first we need to find which items show up in every list for each group of three rucksacks
	# then we can get the sum of those badges' priorities
	return sum(
		get_priority(find_shared(item_lists[i:i + group_size]))
		for i in range(0, len(item_lists), group_size)
	)


def find_shared (item_lists):
	# we can check each item in the first given list to see if any of them appear in all of the other given lists
	shared_item_type = None
	for item_type in item_lists[0]:
		possible = True
		for other_list in item_lists[1:]:
			if item_type not in other_list:
				possible = False
				break
		if possible:
			shared_item_type = item_type
			break
	return shared_item_type


def get_priority (item_type):
	# the priority calculation goes a-zA-Z, so we need to have an offset from the normal char/num conversion
	offset = 38 if item_type.isupper() else 96
	return ord(item_type) - offset


if __name__ == '__main__':
	main('input.txt')
