#!/usr/bin/python3
import re


def main (filepath):
	strings = parse_input(filepath)
	print('part 1:', count_nice(strings, [
		(r'([aeiou])', lambda n: n >= 3),
		(r'(\w)\1', lambda n: n >= 1),
		(r'(ab|cd|pq|xy)', lambda n: n == 0),
	]))
	print('part 2:', count_nice(strings, [
		(r'(\w{2}).*\1', lambda n: n >= 1),
		(r'(\w).\1', lambda n: n >= 1),
	]))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return filehandle.read().strip().split('\n')


def count_nice (strings, rules):
	nice = 0
	for string in strings:
		if all(
			condition(len(re.findall(rule, string)))
			for rule, condition in rules
		):
			nice += 1
	return nice


if __name__ == '__main__':
	main('input.txt')
