#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
numbers = [int(n) for n in filehandle.read().strip().split(',')]
filehandle.close()

seenprior = {}
seenlast = {}
turnlimit = 30000000 if v2 else 2020
number = 0
for turn in range(turnlimit):
	if turn < len(numbers):
		number = numbers[turn]
	elif number in seenprior:
		number = seenlast[number] - seenprior[number]
	else:
		number = 0
	if number in seenlast:
		seenprior[number] = seenlast[number]
	seenlast[number] = turn
print number
