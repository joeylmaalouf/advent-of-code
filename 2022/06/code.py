#!/usr/bin/python3
import copy
import re


def main (filepath):
	characters = parse_input(filepath)
	print('part 1:', find_marker(characters, 4))
	print('part 2:', find_marker(characters, 14))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of characters
		return [
			char
			for char in filehandle.read().strip()
		]


def find_marker (characters, marker_length):
	# the start-of-[packet/message] marker is the first set of characters that all differ
	for i in range(len(characters)):
		if len(set(characters[i : i + marker_length])) == marker_length:
			return i + marker_length


if __name__ == '__main__':
	main('input.txt')
