#!/usr/bin/python

import re

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
rules = re.sub(r'(\.| bags?)', '', filehandle.read().strip()).split('\n')
filehandle.close()

containers = {}
pattern = re.compile(r'^(?:(?P<count>\d+) )?(?P<type>[\w ]+)$')
for rule in rules:
	container, contained = rule.split(' contain ')
	containers[container] = {}
	for listing in contained.split(', '):
		match = pattern.match(listing)
		containers[container][match.group('type')] = int(match.group('count') or 0)

def can_contain(containers, container, containee):
	contained = containers[container].keys()
	if containee in contained:
		return True
	elif contained[0] == 'no other':
		return False
	else:
		return any(can_contain(containers, c, containee) for c in contained)

def contained_bags(containers, container):
	contained = containers[container].keys()
	total = sum(containers[container].values())
	if contained[0] != 'no other':
		total += sum(n * contained_bags(containers, c) for c, n in containers[container].items())
	return total

if v2:
	print contained_bags(containers, 'shiny gold')
else:
	print sum(
		1 if can_contain(containers, container, 'shiny gold') else 0
		for container in containers.keys()
	)
