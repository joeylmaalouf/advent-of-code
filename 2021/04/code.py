#!/usr/bin/python3


def main (filepath, mark):
	values, boards = parse_input(filepath)
	print('part 1:', play_bingo(values, boards, mark, False))
	print('part 2:', play_bingo(values, boards, mark, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of values followed by a series of boards (2D arrays of values)
		sections = filehandle.read().strip().split('\n\n')
		values = sections[0].split(',')
		boards = [[row.split() for row in board.split('\n')] for board in sections[1:]]
		return values, boards


def play_bingo (values, boards, mark, throwing):
	for value in values:
		boards = mark_boards(value, boards, mark)
		for index, board in enumerate(boards):
			if check_winner(board, mark):
				if not throwing:
					return calculate_score(value, board, mark)
				else:
					# if we're throwing the game to let the squid win, we should remove this winning board from our list
					removed = boards.pop(index)
					# and keep going until the final board (the loser board) finishes
					if len(boards) == 0:
						return calculate_score(value, removed, mark)


def mark_boards (value, boards, mark):
	for z, board in enumerate(boards):
		for y, row in enumerate(board):
			for x, val in enumerate(row):
				if val == value:
					boards[z][y][x] = mark
	return boards


def check_winner (board, mark):
	# a winning board is one with all marks in a line

	# first, we'll check the rows
	for row in board:
		if all(val == mark for val in row):
			return True

	# then, we'll check the columns
	for index in range(len(board[0])):
		column = (row[index] for row in board)
		if all(val == mark for val in column):
			return True

	# finally, we'll check the diagonals (JUST KIDDING, WHOOPS, APPARENTLY DIAGONALS DON'T COUNT)
	# for flip in (False, True):
	# 	diagonal = (board[index][(len(board) - 1 - index) if flip else index] for index in range(len(board)))
	# 	if all(val == mark for val in diagonal):
	# 		return True

	# if no full lines were found, this board's not yet a winner
	return False


def calculate_score (value, board, mark):
	# the score is calculated as the sum of the unmarked values left on the board times the final value that finished the bingo
	return int(value) * sum(
		sum(
			0 if val == mark else int(val)
			for val
			in row
		)
		for row
		in board
	)


if __name__ == '__main__':
	main('input.txt', '✔')
