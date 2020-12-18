#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
adapters = sorted([int(n) for n in filehandle.read().strip().split('\n')])
filehandle.close()

gap = 3
first, last = 0, max(adapters) + gap
adapters.insert(0, first)
adapters.append(last)
differences = [adapters[i + 1] - adapters[i] for i in range(0, len(adapters) - 1)]

def valid_alternatives(paths, cache, start, end):
	arrangements = len(paths[start]) - 1 if start in paths.keys() else 0
	if start < end:
		for nextstart in paths[start]:
			if nextstart in cache.keys():
				arrangements += cache[nextstart]
			else:
				alternatives = valid_alternatives(paths, cache, nextstart, end)
				cache[nextstart] = alternatives
				arrangements += alternatives
	return arrangements

if v2:
	paths = {}
	for start in range(0, len(adapters) - 1):
		for end in range(start + 1, len(adapters)):
			if adapters[end] - adapters[start] <= gap:
				if adapters[start] not in paths:
					paths[adapters[start]] = []
				paths[adapters[start]].append(adapters[end])
	start = min(paths.keys())
	end = max([e for ends in paths.values() for e in ends])
	cache = {}
	print 1 + valid_alternatives(paths, cache, start, end)
else:
	print differences.count(1) * differences.count(3)
