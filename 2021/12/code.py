#!/usr/bin/python3


def main (filepath):
	tunnels = parse_input(filepath)
	print('part 1:', len(valid_paths(tunnels, ['start'], [], False)))
	print('part 2:', len(valid_paths(tunnels, ['start'], [], True)))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of connection pairs
		connections = [line.split('-') for line in filehandle.read().strip().split('\n')]
		tunnels = {}
		for connection in connections:
			# we want to set up a map of tunnels from each cave to each potential connecting cave
			for pair in (connection, list(reversed(connection))):
				tunnels[pair[0]] = tunnels.get(pair[0], []) + [pair[1]]
		return tunnels


def valid_paths (tunnels, path, paths, bonus_time):
	# a path is only considered valid if it starts at 'start', ends at 'end', and only visits each small cave (lowercase) at most once
	# valid paths can visit big caves (uppercase) any number of times
	# if we have bonus_time, we can visit one of the small caves twice
	cave = path[-1]
	for connection in tunnels[cave]:
		new_path = path + [connection]
		# if we've reached the end, stop here
		if connection == 'end':
			paths.append(new_path)
		# if we've reached a new cave or a large cave, we'll explore it
		elif connection not in path or connection.isupper():
			paths = valid_paths(tunnels, new_path, paths, bonus_time)
		# if we've reached a small cave we've already been to, we'll only explore it if we have time to do so and it's not the starting cave
		elif bonus_time and connection != 'start':
			paths = valid_paths(tunnels, new_path, paths, False)
	return paths


if __name__ == '__main__':
	main('input.txt')
