#!/usr/bin/python3
import copy
import re


def main (filepath):
	stacks, instructions = parse_input(filepath)
	print('part 1:', get_top_crates(move_crates(copy.deepcopy(stacks), instructions, False)))
	print('part 2:', get_top_crates(move_crates(copy.deepcopy(stacks), instructions, True)))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input comes in two sections: a 2d array of stacks and a list of instructions
		stacks, instructions = filehandle.read().rstrip().split('\n\n')
		# first, we'll extract the stack numbers and give each one its corresponding list of items
		stack_ids = [int(n) for n in stacks.split('\n')[-1].split()]
		stacked_crates = stacks.split('\n')[: -1]
		stacks = {stack_id: [] for stack_id in stack_ids}
		for row in stacked_crates:
			current_stack = 1
			str_index = 1
			while current_stack <= max(stack_ids):
				if not row[str_index].isspace():
					stacks[current_stack].append(row[str_index])
				current_stack += 1
				str_index += 4
		stacks = {stack_id: list(reversed(stack)) for stack_id, stack in stacks.items()}
		# then we'll run each instruction through a regex to pull the relevant numbers
		instr_pattern = re.compile(r'move (?P<amt>\d+) from (?P<src>\d+) to (?P<dst>\d+)')
		instructions = [
			{
				key: int(value)
				for key, value in instr_pattern.match(instruction).groupdict().items()
			}
			for instruction in instructions.split('\n')
		]
		return stacks, instructions


def move_crates (stacks, instructions, in_batches):
	# we can move boxes from stack to stack based on the instructions, either once at a time or in batches
	for instruction in instructions:
		if in_batches:
			batch = stacks[instruction['src']][-instruction['amt']:]
			del stacks[instruction['src']][-(instruction['amt']):]
			stacks[instruction['dst']].extend(batch)
		else:
			for _ in range(instruction['amt']):
				stacks[instruction['dst']].append(stacks[instruction['src']].pop())
	return stacks


def get_top_crates (stacks):
	# we can form a string from the letters matching the top crate in each stack
	return ''.join(stacks[stack_id][-1] for stack_id in sorted(stacks.keys()))


if __name__ == '__main__':
	main('input.txt')
