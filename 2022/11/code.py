#!/usr/bin/python3
import re


def main (filepath):
	notes = parse_input(filepath)
	print('part 1:', watch_rounds(notes, 20, True))
	print('part 2:', watch_rounds(notes, 10000, False))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		notes = []
		# the input is a list of sections of notes that all match a complex pattern
		note_pattern = re.compile(r'Monkey (?P<num>\d+):\s+Starting items: (?P<items>.+)\s+Operation: new = (?P<op>.+)\s+Test: divisible by (?P<divtest>.+)\s+If true: throw to monkey (?P<iftrue>.+)\s+If false: throw to monkey (?P<iffalse>.+)')
		for note in filehandle.read().strip().split('\n\n'):
			note = note_pattern.match(note).groupdict()
			for key in ('num', 'divtest', 'iftrue', 'iffalse'):
				note[key] = int(note[key])
			note['items'] = [int(item) for item in note['items'].split(', ')]
			note['op'] = note['op'].replace('old', 'item')
			notes.append(note)
		return notes


def watch_rounds (notes, rounds, relief):
	items = {note['num']: note['items'][:] for note in notes}
	inspections = {}
	# we need this value for a later optimization
	divtest_prod = 1
	for n in notes:
		divtest_prod *= n['divtest']
	# we want to keep track of how the item worry values and the inspection counts change over a given number of rounds
	for _ in range(rounds):
		items, inspections = play_round(notes, items, inspections, relief, divtest_prod)
	a, b = sorted(inspections.values(), reverse = True)[: 2]
	return a * b


def play_round (notes, items, inspections, relief, divtest_prod):
	# the monkeys will play each round according to our notes
	for monkey in range(max(items.keys()) + 1):
		note = notes[monkey]
		for item in items[monkey]:
			worry = eval(note['op'])
			if relief:
				worry //= 3
			else:
				# technically, the worry values should stay unchanged in this case
				# but if our relief doesn't lower the worry values, the numbers get unreasonably large and the math takes forever
				# so we need this optimization if we want the code to run in any reasonable amount of time
				# /r/adventofcode helped me here, with this value by which we can mod everything and still remain accurate
				worry %= divtest_prod
			throw_to = note['iftrue'] if worry % note['divtest'] == 0 else note['iffalse']
			items[throw_to].append(worry)
			inspections[monkey] = inspections.get(monkey, 0) + 1
		items[monkey] = []
	return items, inspections


if __name__ == '__main__':
	main('input.txt')
