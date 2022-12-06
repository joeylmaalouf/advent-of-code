#!/usr/bin/python3


def main (filepath):
	masses = parse_input(filepath)
	print('part 1:', fuel_total(masses, False))
	print('part 2:', fuel_total(masses, True))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers
		return [
			int(mass)
			for mass in filehandle.read().strip().split('\n')
		]


def fuel_total (masses, recursive):
	# either way we're going to be summing the fuel totals, but we'll do the math differently if the fuel needs fuel for itself
	return sum(
		calc_fuel_recursive(mass) if recursive else calc_fuel(mass)
		for mass in masses
	)


def calc_fuel_recursive (mass):
	fuel = calc_fuel(mass)
	if fuel <= 0:
		return 0
	fuel += calc_fuel_recursive(fuel)
	return fuel


def calc_fuel (mass):
	return mass // 3 - 2


if __name__ == '__main__':
	main('input.txt')
