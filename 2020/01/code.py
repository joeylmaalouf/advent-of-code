#!/usr/bin/python

filepath = 'input.txt'
total = 2020
v2 = False # change to True if doing the second version of the puzzle

filehandle = open(filepath, 'r')
entries = [int(n) for n in filehandle.read().strip().split('\n')]
filehandle.close()

for entry1 in entries:
	for entry2 in entries:
		if v2:
			for entry3 in entries:
				if entry1 + entry2 + entry3 == total:
					print '%d * %d * %d = %d' % (entry1, entry2, entry3, entry1 * entry2 * entry3)
					exit()
		else:
			if entry1 + entry2 == total:
				print '%d * %d = %d' % (entry1, entry2, entry1 * entry2)
				exit()
