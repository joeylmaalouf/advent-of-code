#!/usr/bin/python

from fractions import gcd
from math import ceil

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
earliest, busids = filehandle.read().strip().split('\n')
earliest = int(earliest)
filehandle.close()

def lcm(a, b):
	return abs(a * b) // gcd(a, b)

if v2:
	busids = busids.split(',')
	filtered = []
	for offset, busid in zip(range(0, len(busids)), busids):
		if busid != 'x':
			filtered.append((offset, int(busid)))
	busids = filtered
	increment = busids[0][1]
	timestamp = 0
	furthest = 0
	while True:
		timestamp += increment
		progress = 0
		valid = True
		for offset, busid in busids:
			if (timestamp + offset) % busid != 0:
				valid = False
				break
			progress += 1
		if valid:
			break
		if progress > furthest:
			furthest = progress
			if progress >= 2:
				increment = reduce(lcm, [busid for offset, busid in busids[:progress]], 1)
	print timestamp
else:
	busids = [int(busid) for busid in busids.split(',') if busid != 'x']
	timestamps = [(busid, int(ceil(float(earliest) / busid) * busid)) for busid in busids]
	busid, timestamp = min(timestamps, key = lambda t: t[1])
	print busid * (timestamp - earliest)
