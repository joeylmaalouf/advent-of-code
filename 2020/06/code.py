#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
groups = filehandle.read().strip().split('\n\n')
filehandle.close()

print sum(
	len(
		reduce(
			lambda overlap, member: overlap.intersection(set(member)),
			group.split('\n'),
			set('abcdefghijklmnopqrstuvwxyz')
		) if v2
		else set(group.replace('\n', ''))
	)
	for group in groups
)
