#!/usr/bin/python

from itertools import product
import re

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
instructions = filehandle.read().strip().split('\n')
filehandle.close()

pattern = re.compile(r'mem\[(?P<address>\d+)\]')
mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
memory = {}
for instruction in instructions:
	tokens = instruction.split()
	if tokens[0] == 'mask':
		mask = tokens[2]
	else:
		address = int(pattern.match(tokens[0]).group('address'))
		value = int(tokens[2])
		addressbits = list(format(bin(address)[2:]).zfill(len(mask)))
		valuebits = list(format(bin(value)[2:]).zfill(len(mask)))
		newbits = ['0'] * len(mask)
		addressbitses = []
		if v2:
			for i in range(len(mask)):
				if mask[i] in ('1', 'X'):
					addressbits[i] = mask[i]
			floating = []
			for i in range(len(addressbits)):
				if addressbits[i] == 'X':
					floating.append(i)
			for combination in product('01', repeat = len(floating)):
				newbits = addressbits
				for index, bitval in zip(floating, combination):
					newbits[index] = bitval
				memory[int(''.join(newbits), 2)] = value
		else:
			for i in range(len(mask)):
				if mask[i] != 'X':
					newbits[i] = mask[i]
				else:
					newbits[i] = valuebits[i]
			memory[address] = int(''.join(newbits), 2)
print sum(memory.values())
