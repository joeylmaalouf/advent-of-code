#!/usr/bin/python3


def main (filepath):
	strategy_guide = parse_input(filepath)
	print('part 1:', predict_score(strategy_guide, False))
	print('part 2:', predict_score(strategy_guide, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of [ABC] [XYZ] pairs
		return [
			pair.split(' ')
			for pair in filehandle.read().strip().split('\n')
		]


def predict_score (strategy_guide, target_outcome):
	# we define the maps here instead of inside calculate_points so that we don't recreate them for every round
	matchups = {
		'A': {'C': 'W', 'A': 'D', 'B': 'L'},
		'B': {'A': 'W', 'B': 'D', 'C': 'L'},
		'C': {'B': 'W', 'C': 'D', 'A': 'L'},
	}
	move_points = {
		'A': 1,
		'B': 2,
		'C': 3,
	}
	result_points = {
		'L': 0,
		'D': 3,
		'W': 6,
	}
	# the total score is the sum of each round's results
	return sum(
		calculate_points(*round_moves, matchups, move_points, result_points, target_outcome)
		for round_moves in strategy_guide
	)


def calculate_points (opponent_move, unknown_symbol, matchups, move_points, result_points, target_outcome):
	# if the symbols don't represent the target outcome, we assume they map directly to what we need to throw
	# if the symbols do represent the target outcome, we need to determine what to throw in order to get that outcome
	if not target_outcome:
		# we can convert our XYZ to match the opponent's ABC, then go on and figure out who won
		self_move = {
			'X': 'A',
			'Y': 'B',
			'Z': 'C',
		}[unknown_symbol]
		result = matchups[self_move][opponent_move]
	else:
		# we can convert our XYZ into the round result, then figure out what move we needed to play
		result = {
			'X': 'L',
			'Y': 'D',
			'Z': 'W',
		}[unknown_symbol]
		# since we're working backwards from the opponent's move, we need to flip L and W
		move_matchups = {v: k for k, v in matchups[opponent_move].items()}
		move_matchups['W'], move_matchups['L'] = move_matchups['L'], move_matchups['W']
		self_move = move_matchups[result]

	# points are assigned based on both the actual throw and the round result
	return move_points[self_move] + result_points[result]


if __name__ == '__main__':
	main('input.txt')
