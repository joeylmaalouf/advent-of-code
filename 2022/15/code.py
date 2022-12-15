#!/usr/bin/python3
import multiprocessing
import re


def main (filepath):
	pairs = parse_input(filepath)
	print('part 1:', len(impossible_beacon_positions_along_row(pairs, 2000000)))
	print('part 2:', tuning_frequency(find_distress_beacon(pairs, (0, 0), (4000000, 4000000))))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		pattern = re.compile(r'Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)')
		# the input is a list of sensor-beacon pair coordinates
		return [
			pattern.match(line).groupdict()
			for line in filehandle.read().strip().split('\n')
		]


def impossible_beacon_positions_along_row (pairs, rownum):
	impossible = set()
	for pair in pairs:
		sensor = (int(pair['sensor_x']), int(pair['sensor_y']))
		beacon = (int(pair['beacon_x']), int(pair['beacon_y']))
		search_distance = manhattan_distance(sensor, beacon)
		# if the given row is within our sensor's search radius, we can calculate how far away it is
		# so that we know how much leftover distance we have to move left and right along the given row
		if sensor[1] - search_distance <= rownum and rownum <= sensor[1] + search_distance:
			leftover_distance = search_distance - abs(sensor[1] - rownum)
			for colnum in range(sensor[0] - leftover_distance, sensor[0] + leftover_distance + 1):
				pos = (colnum, rownum)
				if pos != beacon:
					impossible.add(pos)
	return impossible


def manhattan_distance (a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_distress_beacon (pairs, min_bounds, max_bounds):
	# the distress beacon is at the only potential location within the bounds that's not already occupied or marked impossible
	colrange = range(min_bounds[0], max_bounds[0] + 1)
	# we can run multiple processes simultaneously to try to finish faster, but it's still slow
	with multiprocessing.Pool(16) as pool:
		possible = pool.starmap(possible_positions, [
			(pairs, colrange, rownum)
			for rownum in range(min_bounds[1], max_bounds[1] + 1)
		])
		# once we have the list of sets, we can combine them into all the possible beacon positions,
		# then take out the ones with beacons already in them, and then anything left is our distress beacon
		positions = set()
		for options in possible:
			positions = positions.union(options)
		other_beacons = {(int(pair['beacon_x']), int(pair['beacon_y'])) for pair in pairs}
		positions = positions.difference(other_beacons)
		for pos in positions:
			return pos


def possible_positions (pairs, colrange, rownum):
	# the possible positions for any given row are the set of all of them minus the set of ones marked impossible
	potential = {(colnum, rownum) for colnum in colrange}
	impossible = impossible_beacon_positions_along_row(pairs, rownum)
	return potential.difference(impossible)


def tuning_frequency (position):
	return position[0] * 4000000 + position[1]


if __name__ == '__main__':
	main('input.txt')
