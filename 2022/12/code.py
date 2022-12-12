#!/usr/bin/python3


def main (filepath):
	heightmap, start_coords, end_coords = parse_input(filepath)
	print('part 1:', get_path_length(shortest_path(heightmap, start_coords, end_coords)))
	print('part 2:', shortest_path_from_any_start(heightmap, start_coords, end_coords))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a 2D array of elevations
		heightmap = [
			[
				ord(char)
				for char in line
			]
			for line in filehandle.read().strip().split('\n')
		]
		start_coords, end_coords = None, None
		for y in range(len(heightmap)):
			for x in range(len(heightmap[0])):
				if heightmap[y][x] == ord('S'):
					start_coords = (x, y)
					heightmap[y][x] = ord('a')
				elif heightmap[y][x] == ord('E'):
					end_coords = (x, y)
					heightmap[y][x] = ord('z')
		return heightmap, start_coords, end_coords


def shortest_path_from_any_start (heightmap, start_coords, end_coords):
	start_value = heightmap[start_coords[1]][start_coords[0]]
	start_options = {}
	for y in range(len(heightmap)):
		for x in range(len(heightmap[0])):
			# valid starting options are all points with the same elevation as the given start coords
			if heightmap[y][x] == start_value:
				start_option = (x, y)
				path = []
				# there's no need to re-run everything if we already found this starting point along another's path
				seen_in = []
				for cached_path in start_options.values():
					if start_option in cached_path:
						seen_in = cached_path
						break
				if seen_in:
					found_index = seen_in.index(start_option)
					path = seen_in[found_index :]
				else:
					# if we haven't seen this point on an alread-saved shortest path, we'll do the calculations fresh
					path = shortest_path(heightmap, start_option, end_coords)
				if get_path_length(path) != -1:
					start_options[start_option] = path
	return min(get_path_length(p) for p in start_options.values())


def shortest_path (heightmap, start_coords, end_coords):
	# this is just me implementing Dijkstra's algorithm
	path = []
	distances = {} # maps a given point to the shortest distance from the start to that point
	previous = {} # maps a given point to the previous point along the shortest path to that point
	unvisited = set() # for tracking which locations we haven't visited yet
	for y in range(len(heightmap)):
		for x in range(len(heightmap[0])):
			distances[(x, y)] = float('inf')
			unvisited.add((x, y))
	distances[start_coords] = 0
	while len(unvisited) > 0:
		unvisited_distances = {k: v for k, v in distances.items() if k in unvisited}
		closest = min(unvisited_distances, key = unvisited_distances.get)
		unvisited.remove(closest)
		# if the closest unvisited point to the start is the end and it's reachable, we've found our path and can reconstruct it
		if closest == end_coords and end_coords in previous:
			path = construct_path(previous, start_coords, end_coords)
		# we'll check each unvisited neighbor to see if we're on the new shortest route to that point
		for neighbor in get_neighbors(heightmap, closest):
			if neighbor in unvisited:
				new_distance = distances[closest] + 1 # 1 because every step is the same distance here
				if new_distance < distances[neighbor]:
					distances[neighbor] = new_distance
					previous[neighbor] = closest
	return path


def construct_path (previous, start_coords, end_coords):
	path = []
	# we can work our way backwards from the end to the start using the mapping of optimal previous points
	prev = previous[end_coords]
	while prev in previous:
		path.insert(0, prev)
		prev = previous[prev]
	path.insert(0, start_coords)
	path.append(end_coords)
	return path


def get_path_length (path):
	# this could be more complex if we had variable distances, but here it's just the number of steps between points on the path
	return len(path) - 1


def get_neighbors (heightmap, coords):
	neighbors = []
	# we can only move in the cardinal directions
	for movement in [
		(-1, 0),
		(1, 0),
		(0, -1),
		(0, 1),
	]:
		new_x = coords[0] + movement[0]
		new_y = coords[1] + movement[1]
		# to be a valid neighbor, the new location has to be within the map bounds
		# and the elevation has to be at most 1 higher
		if 0 <= new_y and new_y < len(heightmap) \
			and 0 <= new_x and new_x < len(heightmap[0]) \
			and heightmap[new_y][new_x] - heightmap[coords[1]][coords[0]] <= 1:
			neighbors.append((new_x, new_y))
	return neighbors


if __name__ == '__main__':
	main('input.txt')
