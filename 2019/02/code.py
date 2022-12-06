#!/usr/bin/python3
import copy


def main (filepath):
	memory = parse_input(filepath)
	print('part 1:', run_program(memory, 12, 2))
	print('part 2:', find_inputs(memory, 19690720, range(100), range(100)))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers
		return [
			int(mass)
			for mass in filehandle.read().strip().split(',')
		]


def run_program (memory, input1, input2):
	memory = copy.deepcopy(memory) # so that we don't modify the original memory and mess with future program runs
	memory[1 : 3] = (input1, input2)
	# we have to step through the codes in batches, writing new values based on the old ones according to our operation code function map
	functions = {
		1: lambda x, y: x + y,
		2: lambda x, y: x * y,
	}
	i = 0
	while True:
		instruction, param1_address, param2_address, output_address = memory[i : i + 4]
		if instruction == 99:
			return memory[0]
		memory[output_address] = functions[instruction](
			memory[param1_address],
			memory[param2_address],
		)
		i += 4


def find_inputs (memory, target_output, input1_range, input2_range):
	# simple search space
	for input1 in input1_range:
		for input2 in input2_range:
			if run_program(memory, input1, input2) == target_output:
				return 100 * input1 + input2


if __name__ == '__main__':
	main('input.txt')
