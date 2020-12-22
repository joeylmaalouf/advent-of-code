#!/usr/bin/python

from math import ceil

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
earliest, busids = filehandle.read().strip().split('\n')
earliest = int(earliest)
filehandle.close()

if v2:
	busids = busids.split(',')
	filtered = []
	for index, busid in zip(range(0, len(busids)), busids):
		if busid != 'x':
			filtered.append((index, int(busid)))
	busids = filtered
	increment = busids[0][1]
	timestamp = 0
	while True:
		timestamp += increment
		valid = True
		for index, busid in busids:
			if (timestamp + index) % busid != 0:
				valid = False
				break
		if valid:
			break
	print timestamp
else:
	busids = [int(busid) for busid in busids.split(',') if busid != 'x']
	timestamps = [(busid, int(ceil(float(earliest) / busid) * busid)) for busid in busids]
	busid, timestamp = min(timestamps, key = lambda t: t[1])
	print busid * (timestamp - earliest)
