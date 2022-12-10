#!/usr/bin/python3
import math


def main (filepath):
	instructions = parse_input(filepath)
	print('part 1:', sum_signal_strengths(instructions, 20, 40))
	print('part 2:', draw_sprite(instructions, 40, 1))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		instructions = []
		# the input is a list of instructions, optionally with a numeric argument
		for line in filehandle.read().strip().split('\n'):
			(instruction, *args) = line.split()
			instructions.append({
				'instr': instruction,
				'arg': int(args[0]) if len(args) > 0 else None,
			})
		return instructions


def execute_program (instructions):
	# first, we'll process the instructions to account for the cycle delay
	cycle = 0
	operations = {}
	for instruction in instructions:
		if instruction['instr'] == 'noop':
			cycle += 1
		elif instruction['instr'] == 'addx':
			cycle += 2
			operations[cycle] = instruction
	# then we'll run through them, executing the instructions at any cycle with a non-noop operation
	register_values = [1]
	for cycle in range(1, max(operations.keys()) + 1):
		register = register_values[-1]
		if cycle in operations:
			operation = operations[cycle]
			if operation['instr'] == 'addx':
				register += operation['arg']
		register_values.append(register)
	return register_values


def sum_signal_strengths (instructions, starting_cycle, cycle_increment):
	# we want to execute the program and check the signal strengths at the desired points
	register_values = execute_program(instructions)
	signal_strengths = []
	cycle = starting_cycle
	while cycle <= len(register_values):
		# we subtract 1 because the register values are after the given cycle has completed,
		# and we're interested in the value while that cycle is ongoing
		signal_strengths.append(cycle * register_values[cycle - 1])
		cycle += cycle_increment
	return sum(signal_strengths)


def draw_sprite (instructions, line_length, sprite_radius):
	# we want to execute the program and treat the register values as x-positions
	register_values = execute_program(instructions)
	pixels = [
		'#' if abs(cycle % line_length - register_values[cycle]) <= sprite_radius else '.'
		for cycle in range(len(register_values))
	]
	lines = [
		''.join(pixels[i : i + line_length])
		for i in range(0, len(pixels), line_length)
	]
	return '\n' + '\n'.join(lines)


if __name__ == '__main__':
	main('input.txt')
