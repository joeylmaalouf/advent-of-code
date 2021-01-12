#!/usr/bin/python

import re

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
sections = filehandle.read().strip().split('\n\n')
filehandle.close()

rules = sections[0].replace('\"', '').split('\n')
messages = sections[1].split('\n')

rules = {rule.split(': ')[0]: rule.split(': ')[1] for rule in rules}
if v2:
	rules['8'] = '(?: 42 )+?'
	# this isn't the ideal way to do it for 11, but '(42 (?:\1)? 31)' isn't supported by Python
	# and '(?: 42 )+? (?: 31 )+?' wouldn't enforce 42 and 31 the same number of times
	rules['11'] = '42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31'
parsed = {key: False for key in rules}

for key, rule in rules.items():
	letters = [c for c in set(rule.split()) if c.isalpha()]
	if len(letters) > 0:
		rules[key] = letters[0]
		parsed[key] = True
while False in parsed.values():
	for key, rule in rules.items():
		if not parsed[key]:
			contained = [c for c in set(rule.split()) if c.isdigit()]
			if all(parsed[c] for c in contained):
				rule = '|'.join('(?: ' + r + ' )' for r in rule.split('|'))
				index = 0
				tokens = rule.split()
				for token in tokens:
					if token.isdigit():
						tokens[index] = '(?:' + rules[token] + ')' if len(rules[token]) > 1 else rules[token]
					index += 1
				rules[key] = ''.join(tokens)
				parsed[key] = True

pattern = re.compile(r'^' + rules['0'] + r'$')
matches = 0
for message in messages:
	if pattern.search(message):
		matches += 1
print matches
