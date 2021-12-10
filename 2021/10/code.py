#!/usr/bin/python3


def main (filepath):
	lines = parse_input(filepath)
	matches = {
		'(': ')',
		'[': ']',
		'{': '}',
		'<': '>',
	}
	print('part 1:', syntax_error_score(lines, matches))
	print('part 2:', autocomplete_score(lines, matches))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of sets of symbols
		return filehandle.read().strip().split('\n')


def syntax_error_score (lines, matches):
	# the syntax error score is the sum of the point values corresponding to the first illegal character (if any) on each line
	points = {
		None: 0,
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}
	return sum(
		points[process_line(line, matches)[0]]
		for line in lines
	)


def process_line (line, matches):
	# we'll want to keep track of what closing character we expect to see based on what opening characters we've seen
	expected_completions = []
	illegal_close = None
	for char in line:
		# if we've found an opening character, we'll add its matching closing character as our latest expected value
		if char in matches.keys():
			expected_completions.append(matches[char])
		# if we've found a closing character, we'll check whether it's the one we most recently expect
		elif char in matches.values():
			# if it matches, then we can remove that pair from consideration
			if len(expected_completions) > 0 and char == expected_completions[-1]:
				expected_completions.pop()
			# if it doesn't match, we'll remember that value as the first illegal character
			elif not illegal_close:
				illegal_close = char
	# the completion list was created based on the order of the opening characters, so we'll need to reverse it for the closing characters to make sense
	return illegal_close, reversed(expected_completions)


def autocomplete_score (lines, matches):
	points = {
		')': 1,
		']': 2,
		'}': 3,
		'>': 4,
	}
	scores = []
	for line in lines:
		corrupted, completions = process_line(line, matches)
		# autocomplete will only be valid for lines that are not corrupted
		if not corrupted:
			score = 0
			for char in completions:
				score = score * 5 + points[char]
			scores.append(score)
	# the autocomplete score is the middle value of the sorted completion scores
	return sorted(scores)[int(len(scores) / 2)] if scores else 0


if __name__ == '__main__':
	main('input.txt')
