#!/usr/bin/python

v2 = False # change to True if doing the second version of the puzzle
filepath = 'input.txt'

filehandle = open(filepath, 'r')
instructions = filehandle.read().strip().split('\n')
filehandle.close()

def run_instructions(instructions):
	accumulator = 0
	index = 0
	indices = []

	while True:
		if index == len(instructions):
			return True, accumulator
		else:
			operation, argument = instructions[index].split()

		if index in indices:
			return False, accumulator
		else:
			indices.append(index)

		if operation == 'acc':
			accumulator += int(argument)
			index += 1
		elif operation == 'jmp':
			index += int(argument)
		elif operation == 'nop':
			index += 1

if v2:
	index = 0
	for instruction in instructions:
		operation, argument = instruction.split()
		flipoperations = ('jmp', 'nop')
		if operation in flipoperations:
			newinstructions = instructions[:]
			newinstructions[index] = flipoperations[1 - flipoperations.index(operation)] + ' ' + argument
			success, accumulator = run_instructions(newinstructions)
			if success:
				print accumulator
		index += 1
else:
	success, accumulator = run_instructions(instructions)
	print accumulator
