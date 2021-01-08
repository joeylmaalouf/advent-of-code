#!/usr/bin/python

v2 = True # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
equations = filehandle.read().strip().split('\n')
filehandle.close()

operations = {
	'+': lambda x, y: x + y,
	'*': lambda x, y: x * y
}

def prioritize_addition(tokens):
	newtokens = tokens[:]
	for index, token in enumerate(tokens):
		if token == '+':
			if tokens[index - 1].startswith('(') and tokens[index + 1].endswith(')'):
				continue
			if tokens[index - 1].count(')') == 0:
				newtokens[index - 1] = '(' + newtokens[index - 1]
			else:
				opencount = tokens[index - 1].count(')')
				newindex = index - 1
				while opencount > 0:
					newindex -= 1
					opencount += tokens[newindex].count(')')
					opencount -= tokens[newindex].count('(')
				newtokens[newindex] = '(' + newtokens[newindex]
			if tokens[index + 1].count('(') == 0:
				newtokens[index + 1] = newtokens[index + 1] + ')'
			else:
				opencount = tokens[index + 1].count('(')
				newindex = index + 1
				while opencount > 0:
					newindex += 1
					opencount += tokens[newindex].count('(')
					opencount -= tokens[newindex].count(')')
				newtokens[newindex] = newtokens[newindex] + ')'
	return newtokens

def find_groups(tokens):
	groups = []
	opengroups = {}
	depth = 0
	for index, token in enumerate(tokens):
		if token.startswith('('):
			for subtoken in token.split('('):
				if not subtoken.isdigit():
					depth += 1
					opengroups[depth] = index
		if token.endswith(')'):
			for subtoken in token.split(')'):
				if not subtoken.isdigit():
					groups.append([opengroups[depth], index])
					del opengroups[depth]
					depth -= 1
	return groups

def calculate_result(tokens):
	otheropens = tokens[0].count('(') - 1
	tokens[0] = tokens[0].replace('(', '')
	othercloses = tokens[-1].count(')') - 1
	tokens[-1] = tokens[-1].replace(')', '')
	value = int(tokens[0])
	for index in range(1, len(tokens), 2):
		value = operations[tokens[index]](value, int(tokens[index + 1]))
	value = str(value)
	if otheropens > 0:
		value = ('(' * otheropens) + value
	if othercloses > 0:
		value = value + (')' * othercloses)
	return value

total = 0
for equation in equations:
	tokens = equation.split(' ')
	if v2:
		tokens = prioritize_addition(tokens)
	groups = find_groups(tokens)
	groups.append([0, len(tokens) - 1])
	while len(groups) > 0:
		group = groups[0]
		result = calculate_result(tokens[group[0]:group[1] + 1])
		tokens = tokens[:group[0]] + [result] + tokens[group[1] + 1:]
		offset = group[1] - group[0]
		newgroups = []
		for newgroup in groups[1:]:
			if group[1] <= newgroup[0]:
				newgroup[0] -= offset
			if group[1] <= newgroup[1]:
				newgroup[1] -= offset
			newgroups.append(newgroup)
		groups = newgroups
	total += int(tokens[0])
print total
