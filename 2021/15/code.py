#!/usr/bin/python3


def main (filepath):
	risk_map = parse_input(filepath)
	print('part 1:', lowest_risk(risk_map))
	print('part 2:', lowest_risk(scale_map(risk_map, 5)))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a 2D array of numbers
		return [
			[
				int(n)
				for n in line
			] for line in filehandle.read().strip().split('\n')
		]


def lowest_risk (risk_map):
	# this is just my implementation of Dijkstra's algorithm
	start = (0, 0)
	end = (len(risk_map[0]) - 1, len(risk_map) - 1)
	# we'll want to keep track of the risk/cost associated with reaching each point
	risks = {}
	for y in range(len(risk_map)):
		for x in range(len(risk_map[0])):
			risks[(x, y)] = float("inf")
	# it costs us nothing to get to our starting position
	risks[start] = 0
	# we should also keep track of which points we've visited already
	visited = []
	# until we've reached the end, we'll keep going through potential options and figuring out the risk associated with getting to each one
	while risks[end] == float("inf"):
		# in each iteration, we only care about the least risky unvisited point
		point, risk = min(
			risks.items(),
			key = lambda pair: pair[1] if pair[0] not in visited else float("inf")
		)
		visited.append(point)
		# once we have that, we can determine the risk of reaching each adjacent point
		adjacent = []
		if point[0] > 0:
			adjacent.append((point[0] - 1, point[1]))
		if point[0] < len(risk_map[0]) - 1:
			adjacent.append((point[0] + 1, point[1]))
		if point[1] > 0:
			adjacent.append((point[0], point[1] - 1))
		if point[1] < len(risk_map) - 1:
			adjacent.append((point[0], point[1] + 1))
		for adj in adjacent:
			# the risk associated with each point is the total risk we took to get to the previous point plus the risk of the new point itself
			# if we reach a point we've already visited through a different path, we'll priorize the lowest risk path
			risks[adj] = min(risks[adj], risk + risk_map[adj[1]][adj[0]])
	return risks[end]


def scale_map (risk_map, scale):
	new_map = []
	for y_bonus in range(scale):
		for row in risk_map:
			new_row = []
			for x_bonus in range(scale):
				for value in row:
					new_value = (value + x_bonus + y_bonus) % 9
					if new_value == 0:
						new_value = 9
					new_row.append(new_value)
			new_map.append(new_row)
	return new_map


if __name__ == '__main__':
	main('input.txt')
