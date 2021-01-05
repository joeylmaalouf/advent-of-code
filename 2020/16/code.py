#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
sections = filehandle.read().strip().split('\n\n')
filehandle.close()

def parse_ranges(lines):
	ranges = {}
	for line in lines:
		key, rules = line.split(': ')
		ranges[key] = []
		for r in rules.split(' or '):
			ranges[key].append([int(n) for n in r.split('-')])
	return ranges

def parse_ticket(line):
	return [int(n) for n in line.split(',')]

def valid(ranges, value):
	valid = False
	for rangelist in ranges.values():
		for rangepair in rangelist:
			if rangepair[0] <= value and value <= rangepair[1]:
				valid = True
				break
		if valid:
			break
	return valid

def invalid_values(ranges, tickets):
	invalid = []
	for values in tickets:
		for value in values:
			if not valid(ranges, value):
				invalid.append(value)
	return invalid

ranges = parse_ranges(sections[0].split('\n'))
myticket = parse_ticket(sections[1].split('\n')[1])
othertickets = [parse_ticket(line) for line in sections[2].split('\n')[1:]]
if v2:
	tickets = [ticket for ticket in othertickets if all(valid(ranges, value) for value in ticket)]
	potentialkeys = []
	for index in range(len(myticket)):
		potentialkeys.append(ranges.keys()[:])
		for key, rangelist in ranges.items():
			for ticket in tickets:
				value = ticket[index]
				valid = any(rangepair[0] <= value and value <= rangepair[1] for rangepair in rangelist)
				if not valid:
					potentialkeys[index].remove(key)
					break
	index = 0
	while any(len(options) != 1 for options in potentialkeys):
		index = (index + 1) % len(potentialkeys)
		if len(potentialkeys[index]) == 1:
			key = potentialkeys[index][0]
			for otherindex in range(len(potentialkeys)):
				if index != otherindex and key in potentialkeys[otherindex]:
					potentialkeys[otherindex].remove(key)
	keys = [options[0] for options in potentialkeys]
	departurevalues = [myticket[index] for index, key in enumerate(keys) if key.startswith('departure')]
	print reduce(lambda x, y: x * y, departurevalues, 1)
else:
	print sum(invalid_values(ranges, othertickets))
