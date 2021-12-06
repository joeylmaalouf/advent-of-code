#!/usr/bin/python3


def main (filepath):
	timers = parse_input(filepath)
	print('part 1:', simulate_fish(timers, 8, 6, 80))
	print('part 2:', simulate_fish(timers, 8, 6, 256))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of numbers
		return [int(value) for value in filehandle.read().strip().split(',')]


def simulate_fish (timers, max_timer, reset_timer, iterations):
	# we first want to transform the list of timers into a mapping of each timer value to the count of fish that match it
	timer_counts = {timer: 0 for timer in range(max_timer + 1)}
	for timer in timers:
		timer_counts[timer] += 1
	# this way, our step operation becomes significantly more efficient, since it can operate on the counts rather than iterate over every timer individually
	for _ in range(iterations):
		timer_counts = step(timer_counts, max_timer, reset_timer)
	return sum(timer_counts.values())


def step (timer_counts, max_timer, reset_timer):
	# we first need to shift every count downwards by 1 step
	for timer in range(max_timer + 1):
		timer_counts[timer - 1] = timer_counts[timer]
	timer_counts[max_timer] = 0
	# then we reset any timers that made it below 0 to the reset value while also adding their newborn fish at the maximum value
	births = timer_counts.pop(-1)
	timer_counts[reset_timer] += births
	timer_counts[max_timer] += births
	return timer_counts


if __name__ == '__main__':
	main('input.txt')
