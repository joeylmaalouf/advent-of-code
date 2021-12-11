#!/usr/bin/python3


def main (filepath):
	print('part 1:', check_flashes(parse_input(filepath), 100, False))
	print('part 2:', check_flashes(parse_input(filepath), 1000, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a 2D array of numbers
		return [
			[
				int(n)
				for n in line
			] for line in filehandle.read().strip().split('\n')
		]


def check_flashes (energy_levels, steps, check_simultaneous):
	flashes = 0
	for step in range(steps):
		# first, each octopus gains energy naturally
		passive_gain(energy_levels)
		# # then, we'll keep checking whether any of them flashed and giving energy to those adjacent until there are no more at flash level
		while any(
			any(
				value != 'F' and value > 9
				for value in row
			) for row in energy_levels
		):
			flashes += get_flashing(energy_levels)
		# once that's all measured, we'll reset any that flashed
		reset_flashed(energy_levels)
		# finally, if we wanted to check whether the octopi all flashed simultaneously, we'll do that last
		if check_simultaneous and all(all(value == 0 for value in row) for row in energy_levels):
			return step + 1
	return flashes


def passive_gain (energy_levels):
	for y, row in enumerate(energy_levels):
		for x, _ in enumerate(row):
			energy_levels[y][x] += 1


def get_flashing (energy_levels):
	flashes = 0
	for y, row in enumerate(energy_levels):
		for x, _ in enumerate(row):
			# any octopus that isn't already marked as flashing and has enough energy to flash should be marked as flashing
			if energy_levels[y][x] != 'F' and energy_levels[y][x] > 9:
				flashes += 1
				energy_levels[y][x] = 'F'
				# and its flash should power adjacent octopi, which we then need to check again (in case this was the last bit of power they needed to flash)
				for ny in range(max(y - 1, 0), min(y + 2, len(energy_levels))):
					for nx in range(max(x - 1, 0), min(x + 2, len(energy_levels[0]))):
						if (nx != x or ny != y) and energy_levels[ny][nx] != 'F':
							energy_levels[ny][nx] += 1
							flashes += get_flashing(energy_levels)
	return flashes


def reset_flashed (energy_levels):
	for y, row in enumerate(energy_levels):
		for x, value in enumerate(row):
			if value == 'F':
				energy_levels[y][x] = 0


if __name__ == '__main__':
	main('input.txt')
